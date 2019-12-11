from defs import *
from values import *
import math
import flux
import copy
import numpy as np

# parameters
dx = 1e-3
PI = 3.14159265
cell  = membrane()
celln = membrane()

count=0

def conservation_init (my_cell0, my_cell1,my_celln, my_dx):

    # global parameters
    global dx
    global cell0,cell1,cellm,celln

    cell0  = copy.deepcopy(my_cell0)
    cell1  = copy.deepcopy(my_cell1)
    celln = copy.deepcopy(my_celln)
    dx    = my_dx


#----------------------------------------------------------------------------
# compute residuals of conservation equations
# inputs:
#  cell:  current cell values
#  celln: cell function values at previous time-step
#  dx:    time-step
# returns:
#  fvec:  residuals
#
# no. of unknowns = no. of solutes, in cell and in LIS, plus 4 membrane
#  potentials (lumen-cell/LIS, cell/LIS-bath)
#----------------------------------------------------------------------------

def conservation_eqs (x,i):
    dt=1
    Jvol1=np.zeros(NC*NC).reshape(NC,NC)
    Jsol1=np.zeros(NS*NC*NC).reshape(NS,NC,NC)

    if cell1.segment == 'PT' or cell1.segment == 'S3' or cell1.segment == 'mTAL' or cell1.segment == 'cTAL' or cell1.segment == 'MD' or cell1.segment == 'DCT' or cell1.segment =='SDL' or cell1.segment == 'IMCD':

        cell1.conc[:,0] = x[0:NS]
        cell1.conc[:,1] = x[NS:2*NS]
        cell1.conc[:,4] = x[2*NS:3*NS]

        cell1.vol[0] = x[3*NS]
        cell1.vol[1]=x[3*NS+1]
        cell1.vol[4] = x[3*NS+2]

        cell1.ep[0] = x[3*NS+3]
        cell1.ep[1] = x[3*NS+4]
        cell1.ep[4] = x[3*NS+5]

        cell1.pres[0] = x[3*NS+6]
        # cell1.pres[1]=x[3*NS+6]

        ph = np.zeros(NC)

        for j in [0,1,4]:
            ph[j] = -np.log(abs(cell1.conc[11][j])/1e3)/np.log(10.0)

        Bm = PI*cell1.diam
        Am = PI*(cell1.diam**2)/4

        if cell1.segment == 'IMCD':
            coalesce = 0.2*(1-0.95*(i/N)**2)*np.exp(-2.75*i/N)
            Bm = Bm*coalesce
            Am = Am*coalesce


        fsol0 = np.zeros(NS)
        fsol1 = np.zeros(NS)

        for j in range(NS):
            fsol0[j] = celln.conc[j][0]*celln.vol[0]*Vref/href
            fsol1[j] = cell1.conc[j][0]*cell1.vol[0]*Vref/href

        fvol0 = cell0.vol[0]*Vref
        fvol1 = cell1.vol[0]*Vref

        PM0 = celln.pres[0]
        PM1 = x[3*NS+6]

        Jvol1,Jsol1 = flux.compute_fluxes(cell1,i)

    #---------------------------------------------------------------------
    #   Initialize  source terms
    #---------------------------------------------------------------------
        fvec = np.zeros(3*NS+7)          # conservation for individual solutes
        S    = np.zeros(3*NS+7)          # reaction terms

    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #   COMPUTE SOURCE TERMS FOR FLOW OF SOLUTE I IN THE LUMEN
    #   The non-dimensional volume flux needs to be multiplied by
    #    (Vref/href)
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
        for j in range(NS):
            sumJsol1 = Jsol1[j,0,1]+Jsol1[j,0,4]
            fsola = celln.vol[0]*celln.conc[j][0]*Vref/href
            fsolb = cell1.vol[0]*cell1.conc[j][0]*Vref/href
            S[3*j] = fsolb-fsola+Bm*cell1.len*sumJsol1/cell1.total+Am*(cell1.conc[j,0]-cell0.conc[j,0])*(cell1.len/cell1.total)/dt
            # if i == 0:
            # 	print(Jsol1[i,0,1],Jsol1[i,0,4])
            # 	print(fsolb,fsola,Bm,cell1.len,sumJsol1)

    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #	COMPUTE SOURCE TERMS FOR SOLUTE I IN EACH CELLULAR COMPARTMENT
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------



        for j in range(NS):
            S[1+3*j] = -Jsol1[j][0][1]+Jsol1[j][1][4]+Jsol1[j][1][5]
            S[2+3*j] = -Jsol1[j][1][4]-Jsol1[j][0][4]+Jsol1[j][4][5]
        #print(Jsol1[2,1,4],Jsol1[2,1,5],Jsol1[2,0,1])

    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #   COMPUTE SOURCE TERMS FOR VOLUME FLOW IN THE LUMEN
    #   The non-dimensional volume flux needs to be multiplied by
    #   Vref/(Pfref.Vwbar.Cref)
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
        fvmult = Pfref*Vwbar*Cref
        sumJvol1 = (Jvol1[0,1]+Jvol1[0,4])*fvmult
        fvola = celln.vol[0]*Vref
        fvolb = cell1.vol[0]*Vref
        S[3*NS] = fvolb-fvola+Bm*cell1.len*sumJvol1/cell1.total

    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #   COMPUTE SOURCE TERMS FOR VOLUME IN EACH CELLULAR COMPARTMENT
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------

        S[1+3*NS] = Jvol1[1,4]+Jvol1[1,5]-Jvol1[0,1]
        S[2+3*NS] = Jvol1[4,5]-Jvol1[0,4]-Jvol1[1,4]

    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #   Convert to equations of the form F(X) = 0
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------

    #---------------------------------------------------------------------
    #    For I = 1-3 and 9 (non-reacting solutes)
    #---------------------------------------------------------------------
        for m in [0,1,2,8,14]:
            fvec[3*m]=S[3*m]
            fvec[3 * m+1] = S[3 * m+1]+(cell1.vol[1]*cell1.conc[m,1]-cell0.vol[1]*cell0.conc[m,1])/dt
            fvec[3 * m+2] = S[3 * m+2]+(cell1.vol[4]*cell1.conc[m,4]-cell0.vol[4]*cell0.conc[m,4])/dt



    #HCO2-/H2CO2 equations modified

        # for m in range(12,15):
        # 	fvec[3*m]=S[3*m]
        # 	fvec[1+3*m]=S[1+3*m]
        # 	fvec[2+3*m]=S[2+3*m]


    #---------------------------------------------------------------------
    #    For CO2/HCO3/H2CO3
    #    The dimensional factor for the kinetic term in the lumen is
    #    Am/Bm = Pi R^2 / 2 PI R = R / 2 = D / 4
    #---------------------------------------------------------------------

        fvec[9] = S[9]+S[12]+S[15]
        fvec[10] = S[10]+S[13]+S[16]+(cell1.vol[1]*(cell1.conc[3,1]+cell1.conc[4,1]+cell1.conc[5,1])-cell0.vol[1]*(cell0.conc[3,1]+cell0.conc[4,1]+cell0.conc[5,1]))/dt
        fvec[11] = S[11]+S[14]+S[17]+(cell1.vol[4]*(cell1.conc[3,4]+cell1.conc[4,4]+cell1.conc[5,4])-cell0.vol[4]*(cell0.conc[3,4]+cell0.conc[4,4]+cell0.conc[5,4]))/dt
        fvec[12] = ph[0]-pKHCO3-np.log(abs(float(cell1.conc[3,0])/float(cell1.conc[4,0])))/np.log(10.0)
        fvec[13] = ph[1]-pKHCO3-np.log(abs(float(cell1.conc[3,1])/float(cell1.conc[4,1])))/np.log(10.0)
        fvec[14] = ph[4]-pKHCO3-np.log(abs(float(cell1.conc[3,4])/float(cell1.conc[4,4])))/np.log(10.0)

        #print(ph[0],pKHCO3,cell1.conc[3,0],cell1.conc[4,0])

        fkin1=(cell1.dkh[0]*celln.conc[5,0]-cell1.dkd[0]*celln.conc[4,0])
        fkin2=(cell1.dkh[0]*cell1.conc[5,0]-cell1.dkd[0]*cell1.conc[4,0])
        fvec[15] = S[15] + Am*cell1.len*fkin2/cell1.total/href
  
    #print(S[15],Am,cell1.len,fkin2,cell1.total,href)
    #print(cell1.dkh[0],cell1.conc[5,0],cell1.dkd[0],cell1.conc[4,0])

        facnd=Vref/href
        fvec[16] = S[16]+cell1.vol[1]*(cell1.dkh[1]*cell1.conc[5,1]-cell1.dkd[1]*cell1.conc[4,1])*facnd+(cell1.vol[1]*cell1.conc[5,1]-cell0.vol[1]*cell0.conc[5,1])/dt
        fvec[17] = S[17]+max(cell1.vol[4],cell1.volref[4])*(cell1.dkh[4]*cell1.conc[5,4]-cell1.dkd[4]*cell1.conc[4,4])*facnd+(cell1.vol[4]*cell1.conc[5,4]-cell0.vol[4]*cell0.conc[5,4])/dt

    #---------------------------------------------------------------------
    #    For HPO4(2-)/H2PO4(-)
    #---------------------------------------------------------------------

        fvec[18] = S[18]+S[21]
        fvec[19] = S[19]+S[22]+(cell1.vol[1]*(cell1.conc[6,1]+cell1.conc[7,1])-cell0.vol[1]*(cell0.conc[6,1]+cell0.conc[7,1]))/dt
        fvec[20] = S[20]+S[23]+(cell1.vol[4]*(cell1.conc[6,4]+cell1.conc[7,4])-cell0.vol[4]*(cell0.conc[6,4]+cell0.conc[7,4]))/dt
        fvec[21] = ph[0]-pKHPO4-np.log(abs(float(cell1.conc[6,0])/float(cell1.conc[7,0])))/np.log(10.0)
        fvec[22] = ph[1]-pKHPO4-np.log(abs(float(cell1.conc[6,1])/float(cell1.conc[7,1])))/np.log(10.0)
        fvec[23] = ph[4]-pKHPO4-np.log(abs(float(cell1.conc[6,4])/float(cell1.conc[7,4])))/np.log(10.0)

    #---------------------------------------------------------------------
    #    For NH3/NH4
    #---------------------------------------------------------------------
        if cell1.segment == 'PT' or cell1.segment == 'S3':
            if cell1.segment == 'PT':
                TS = 1.3
                scaleT = 1.0
            elif cell1.segment == 'S3':
                TS = 1.3    # In fortran code it's a half of PCT (=0.6), but for more reseaonable results it's ok to modify it to any value
                scaleT = 0.5

    #torque-modulated effects

            PM=cell1.pres[0]

            Radref = 0.0025/2.0e0
            fac1 = 8.0*visc*(cell1.vol_init[0]*Vref)*torqL/(Radref**2)
            fac2 = 1.0 + (torqL+torqd)/Radref + 0.50*((torqL/Radref)**2)
            TM0= fac1*fac2

            RMtorq = torqR*(1.0e0+torqvm*(PM - PbloodPT))
            factor1 = 8.0*visc*(cell1.vol[0]*Vref)*torqL/(RMtorq**2)
            factor2 = 1.0 + (torqL+torqd)/RMtorq + 0.50*((torqL/RMtorq)**2)
            Torque = factor1*factor2

            Scaletorq = 1.0 + TS*scaleT*(Torque/TM0-1.0)

            Qnh4 = 0.25e-6/(href*Cref)*Scaletorq
        else:
            Qnh4 = 0.0

        fvec[27] = S[27]+S[30]
        fvec[28] = S[28]+S[31]-Qnh4+(cell1.vol[1]*(cell1.conc[9,1]+cell1.conc[10,1])-cell0.vol[1]*(cell0.conc[9,1]+cell0.conc[10,1]))/dt
        fvec[29] = S[29]+S[32]+(cell1.vol[4]*(cell1.conc[9,4]+cell1.conc[10,4])-cell0.vol[4]*(cell0.conc[9,4]+cell0.conc[10,4]))/dt
        fvec[30] = ph[0]-pKNH3-np.log(abs(float(cell1.conc[9,0])/float(cell1.conc[10,0])))/np.log(10.0)
        fvec[31] = ph[1]-pKNH3-np.log(abs(float(cell1.conc[9,1])/float(cell1.conc[10,1])))/np.log(10.0)
        fvec[32] = ph[4]-pKNH3-np.log(abs(float(cell1.conc[9,4])/float(cell1.conc[10,4])))/np.log(10.0)

        #print(ph[0],pKNH3,cell1.conc[9,0],cell1.conc[10,0])
    #---------------------------------------------------------------------
    #    For HCO2-/H2CO2
    #---------------------------------------------------------------------

        fvec[36] = S[36]+S[39]
        fvec[37] = S[37]+S[40]+(cell1.vol[1]*(cell1.conc[12,1]+cell1.conc[13,1])-cell0.vol[1]*(cell0.conc[12,1]+cell0.conc[13,1]))/dt
        fvec[38] = S[38]+S[41]+(cell1.vol[4]*(cell1.conc[12,4]+cell1.conc[13,4])-cell0.vol[4]*(cell0.conc[12,4]+cell0.conc[13,4]))/dt
        fvec[39] = ph[0]-pKHCO2-np.log(cell1.conc[12,0]/cell1.conc[13,0])/np.log(10.0)
        if cell1.segment == 'PT' or cell1.segment == 'S3':
            fvec[40] = ph[1]-pKHCO2-np.log(cell1.conc[12,1]/cell1.conc[13,1])/np.log(10.0)
        fvec[41] = ph[4]-pKHCO2-np.log(cell1.conc[12,4]/cell1.conc[13,4])/np.log(10.0)

        #print(ph[1],pKHCO2,cell1.conc[12,1],cell1.conc[13,1])

    #---------------------------------------------------------------------
    #    For pH
    #---------------------------------------------------------------------
        fvec[33] = S[33]+S[30]-S[18]-S[9]-S[36]
        fvec[34] = S[34]+S[31]-S[19]-S[10]-S[37]+(cell1.vol[1]*(cell1.conc[11,1]+cell1.conc[10,1]-cell1.conc[6,1]-cell1.conc[3,1]-cell1.conc[12,1])-cell0.vol[1]*(cell0.conc[11,1]+cell0.conc[10,1]-cell0.conc[6,1]-cell0.conc[3,1]-cell0.conc[12,1]))/dt
        fvec[35] = S[35]+S[32]-S[20]-S[11]-S[38]+(cell1.vol[4]*(cell1.conc[11,4]+cell1.conc[10,4]-cell1.conc[6,4]-cell1.conc[3,4]-cell1.conc[12,4])-cell0.vol[4]*(cell0.conc[11,4]+cell0.conc[10,4]-cell0.conc[6,4]-cell0.conc[3,4]-cell0.conc[12,4]))/dt

    #---------------------------------------------------------------------
    #    For volume
    #---------------------------------------------------------------------

        fvec[3*NS]=S[3*NS]
        fvec[1+3*NS]=S[1+3*NS]+(cell1.vol[1]-cell0.vol[1])/dt
        fvec[2+3*NS]=S[2+3*NS]+(cell1.vol[4]-cell0.vol[4])/dt


    #---------------------------------------------------------------------72
    #	 For EP, need to satisfy electroneutrality
    #---------------------------------------------------------------------72

        currM = 0
        for j in range(NS):
            currM = currM+zval[j]*(Jsol1[j,0,1]+Jsol1[j,0,4])
        fvec[3+3*NS]=currM

        volPrat=cell1.volref[1]/cell1.vol[1]
        CimpP=cell1.cimpref[1]*volPrat
        facP=np.exp(np.log(10.0)*(ph[1]-pKbuf))
    # need to fix totBuf, allow to be different from [imp]
        totBuf = cell1.cimpref[1]
        if cell1.segment=='DCT':
            totBuf=CPbuftotD
        elif cell1.segment == 'IMCD':
            totBuf=CPbuftotIMC
        else:
            totBuf=cell1.cimpref[1]
        CbufP=totBuf*volPrat*facP/(facP+1)

        elecP= -CimpP-CbufP
        elecE=0

        for j in range(NS):
            elecP=elecP+zval[j]*cell1.conc[j,1]
            elecE=elecE+zval[j]*cell1.conc[j,4]

        fvec[4+3*NS]=elecP
        fvec[5+3*NS]=elecE

#---------------------------------------------------------------------72
#	 For Pressure
#---------------------------------------------------------------------72    

        RMcompl = torqR*(1.0e0+torqvm*(cell1.pres[0] - PbloodPT))
        Amcompl = PI*(RMcompl**2)
        if cell1.segment == 'IMCD':
            factor1 = 8.0*PI*visc/(Am**2)
        else:
            factor1 = 8.0e0*PI*visc/(Amcompl**2)
        if cell1.segment == 'IMCD':
            factor1 = factor1*coalesce*2
        fvec[6+3*NS] = PM1-PM0+factor1*cell1.vol[0]*Vref*cell1.len/cell1.total
        #print(PM1,PM0,factor1,cell1.vol[0])

    elif cell1.segment == 'CNT' or cell1.segment == 'CCD' or cell1.segment == 'OMCD':
        for j in range(NS):
            cell1.conc[j,0] = x[5*j]
            cell1.conc[j,1] = x[5*j+1]
            cell1.conc[j,2] = x[5*j+2]
            cell1.conc[j,3] = x[5*j+3]
            cell1.conc[j,4] = x[5*j+4]

        for j in range(NC-1):
            cell1.vol[j]=x[5*NS+j]
            cell1.ep[j]=x[5*NS+5+j]
        cell1.pres[0]=x[5*NS+10]
        ph = np.zeros(NC)
        for j in range(NC):
            ph[j] = -np.log(abs(cell1.conc[11][j])/1.0e3)/np.log(10.0)

        #think about where to put this parameter
        if cell1.segment == 'CNT':
            coalesce = 2.0**(-2.32*(i+1)/cell1.total)
        elif cell1.segment == 'CCD' or cell1.segment == 'OMCD':
            coalesce = 0.2
        else:
            coalesce = 1.0

        Bm = PI*cell1.diam*coalesce
        Am = PI*(cell1.diam**2)/4.0*coalesce

        Jvol1,Jsol1 = flux.compute_fluxes(cell1,i)
        #Jvol0,Jsol0 = flux.compute_fluxes(cell0,i)

    #-------------------------------------------------------------------------
    # Initialize source terms
    #-------------------------------------------------------------------------
        fvec = np.zeros(5*NS+11)			# conservation for individual solutes
        S = np.zeros(5*NS+11)				# reaction terms

    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #   COMPUTE SOURCE TERMS FOR FLOW OF SOLUTE I IN THE LUMINAL AND CELLULAR COMPARTMENT
    #   The non-dimensional volume flux needs to be multiplied by
    #    (Vref/href)
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
        for j in range(NS):
            #sumJsa = Jsol0[i,0,1]+Jsol0[i,0,2]+Jsol0[i,0,3]+Jsol0[i,0,4]
            if cell1.segment == 'OMCD':
                sumJsb = Jsol1[j,0,1]+Jsol1[j,0,2]+Jsol1[j,0,4]
            else:
                sumJsb = Jsol1[j,0,1]+Jsol1[j,0,2]+Jsol1[j,0,3]+Jsol1[j,0,4]
            fsola = cell0.vol[0]*cell0.conc[j,0]*Vref/href
            fsolb = cell1.vol[0]*cell1.conc[j,0]*Vref/href
            S[5*j] = fsolb-fsola+Bm*cell1.len*sumJsb/cell1.total
            S[5*j+1] = Jsol1[j,1,4]+Jsol1[j,1,5]-Jsol1[j,0,1]
            S[5*j+2] = Jsol1[j,2,4]+Jsol1[j,2,5]-Jsol1[j,0,2]
            S[5*j+3] = Jsol1[j,3,4]+Jsol1[j,3,5]-Jsol1[j,0,3]
            if cell1.segment == 'OMCD':
                S[5*j+4] = -Jsol1[j,0,4]-Jsol1[j,1,4]-Jsol1[j,2,4]+Jsol1[j,4,5]
            else:
                S[5*j+4] = -Jsol1[j,0,4]-Jsol1[j,1,4]-Jsol1[j,2,4]-Jsol1[j,3,4]+Jsol1[j,4,5]

    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #   COMPUTE SOURCE TERMS FOR VOLUME FLOW IN THE LUMEN
    #   The non-dimensional volume flux needs to be multiplied by
    #   Vref/(Pfref.Vwbar.Cref)
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
        fvmult = (Pfref*Vwbar*Cref)
        sumJvb = (Jvol1[0,1]+Jvol1[0,2]+Jvol1[0,3]+Jvol1[0,4])*fvmult
        fvola = cell0.vol[0]*Vref
        fvolb = cell1.vol[0]*Vref

        S[5*NS] = fvolb-fvola+Bm*cell1.len*sumJvb/cell1.total

    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #   COMPUTE SOURCE TERMS FOR VOLUME IN EACH CELLULAR COMPARTMENT
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
        S[5*NS+1] = Jvol1[1,4]+Jvol1[1,5]-Jvol1[0,1]
        S[5*NS+2] = Jvol1[2,4]+Jvol1[2,5]-Jvol1[0,2]
        S[5*NS+3] = Jvol1[3,4]+Jvol1[3,5]-Jvol1[0,3]
        if cell1.segment == 'OMCD':
            S[5*NS+4] = -Jvol1[0,4]-Jvol1[1,4]-Jvol1[2,4]+Jvol1[4,5]
        else:
            S[5*NS+4] = -Jvol1[0,4]-Jvol1[1,4]-Jvol1[2,4]-Jvol1[3,4]+Jvol1[4,5]

    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #   Convert to equations of the form F(X) = 0
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------

    #---------------------------------------------------------------------
    #    For I = 1-3 and 9 (non-reacting solutes)
    #---------------------------------------------------------------------
        for m in range(15):
            fvec[m] = S[m]

        fvec[40] = S[40]
        fvec[41] = S[41]
        fvec[42] = S[42]
        fvec[43] = S[43]
        fvec[44] = S[44]
    #----------------------------------------------------------------------
    #	HCO2-/H2CO2 equations modified
    #----------------------------------------------------------------------
        for m in range(12,15):
            fvec[5*m] = S[5*m]
            fvec[5*m+1] = S[5*m+1]
            fvec[5*m+2] = S[5*m+2]
            if cell1.segment == 'OMCD':
                fvec[5*m+3] = cell1.conc[m,3]-cell1.conc[m,2]
            else:
                fvec[5*m+3] = S[5*m+3]
            fvec[5*m+4] = S[5*m+4]
    #----------------------------------------------------------------------
        if cell1.segment == 'OMCD':
            fvec[40] = S[40]
            fvec[41] = S[41]
            fvec[42] = S[42]
            fvec[44] = S[44]

            fvec[3] = cell1.conc[0,3]-cell1.conc[0,2]
            fvec[8] = cell1.conc[1,3]-cell1.conc[1,2]
            fvec[13] = cell1.conc[2,3]-cell1.conc[2,2]
            fvec[43] = cell1.conc[8,3]-cell1.conc[8,2]

    #---------------------------------------------------------------------
    #    For CO2/HCO3/H2CO3
    #    The dimensional factor for the kinetic term in the lumen is
    #    Am/Bm = Pi R^2 / 2 PI R = R / 2 = D / 4
    #---------------------------------------------------------------------
        fvec[15] = S[15]+S[20]+S[25]
        fvec[16] = S[16]+S[21]+S[26]
        fvec[17] = S[17]+S[22]+S[27]
        if cell1.segment == 'OMCD':
            fvec[18] = cell1.conc[3,3]-cell1.conc[3,2]
        else:
            fvec[18] = S[18]+S[23]+S[28]
        fvec[19] = S[19]+S[24]+S[29]
        fvec[20] = ph[0]-pKHCO3-np.log(abs(float(cell1.conc[3,0])/float(cell1.conc[4,0])))/np.log(10.0)
        fvec[21] = ph[1]-pKHCO3-np.log(abs(float(cell1.conc[3,1])/float(cell1.conc[4,1])))/np.log(10.0)
        fvec[22] = ph[2]-pKHCO3-np.log(abs(float(cell1.conc[3,2])/float(cell1.conc[4,2])))/np.log(10.0)
        if cell1.segment == 'OMCD':
            fvec[23] = cell1.conc[4,3]-cell1.conc[4,2]
        else:
            fvec[23] = ph[3]-pKHCO3-np.log(abs(float(cell1.conc[3,3])/float(cell1.conc[4,3])))/np.log(10.0)
        fvec[24] = ph[4]-pKHCO3-np.log(abs(float(cell1.conc[3,4])/float(cell1.conc[4,4])))/np.log(10.0)

        fkin2 = cell1.dkh[0]*cell1.conc[5,0]-cell1.dkd[0]*cell1.conc[4,0]
        fvec[25] = S[25]+Am*cell1.len*fkin2/cell1.total/href

        facnd = Vref/href
        fvec[26] = S[26]+cell1.vol[1]*(cell1.dkh[1]*cell1.conc[5,1]-cell1.dkd[1]*cell1.conc[4,1])*facnd
        fvec[27] = S[27]+cell1.vol[2]*(cell1.dkh[2]*cell1.conc[5,2]-cell1.dkd[2]*cell1.conc[4,2])*facnd
        if cell1.segment == 'OMCD':
            fvec[28] = cell1.conc[5,3]-cell1.conc[5,2]
        else:
            fvec[28] = S[28]+cell1.vol[3]*(cell1.dkh[3]*cell1.conc[5,3]-cell1.dkd[3]*cell1.conc[4,3])*facnd
        fvec[29] = S[29]+max(cell1.vol[4],cell1.volref[4])*(cell1.dkh[4]*cell1.conc[5,4]-cell1.dkd[4]*cell1.conc[4,4])*facnd

    #---------------------------------------------------------------------
    #    For HPO4(2-)/H2PO4(-)
    #---------------------------------------------------------------------
        fvec[30] = S[30]+S[35]
        fvec[31] = S[31]+S[36]
        fvec[32] = S[32]+S[37]
        if cell1.segment == 'OMCD':
            fvec[33] = cell1.conc[6,3]-cell1.conc[6,2]
        else:
            fvec[33] = S[33]+S[38]
        fvec[34] = S[34]+S[39]
        fvec[35] = ph[0]-pKHPO4-np.log(abs(float(cell1.conc[6,0])/float(cell1.conc[7,0])))/np.log(10.0)
        fvec[36] = ph[1]-pKHPO4-np.log(abs(float(cell1.conc[6,1])/float(cell1.conc[7,1])))/np.log(10.0)
        fvec[37] = ph[2]-pKHPO4-np.log(abs(float(cell1.conc[6,2])/float(cell1.conc[7,2])))/np.log(10.0)
        if cell1.segment == 'OMCD':
            fvec[38] = cell1.conc[7,3]-cell1.conc[7,2]
        else:
            fvec[38] = ph[3]-pKHPO4-np.log(abs(float(cell1.conc[6,3])/float(cell1.conc[7,3])))/np.log(10.0)
        fvec[39] = ph[4]-pKHPO4-np.log(abs(float(cell1.conc[6,4])/float(cell1.conc[7,4])))/np.log(10.0)
    #---------------------------------------------------------------------
    #    For NH3/NH4
    #---------------------------------------------------------------------
        fvec[45] = S[45]+S[50]
        fvec[46] = S[46]+S[51]
        fvec[47] = S[47]+S[52]
        if cell1.segment == 'OMCD':
            fvec[48] = cell1.conc[9,3]-cell1.conc[9,2]
        else:
            fvec[48] = S[48]+S[53]
        fvec[49] = S[49]+S[54]
        fvec[50] = ph[0]-pKNH3-np.log(abs(float(cell1.conc[9,0])/float(cell1.conc[10,0])))/np.log(10.0)
        fvec[51] = ph[1]-pKNH3-np.log(abs(float(cell1.conc[9,1])/float(cell1.conc[10,1])))/np.log(10.0)
        fvec[52] = ph[2]-pKNH3-np.log(abs(float(cell1.conc[9,2])/float(cell1.conc[10,2])))/np.log(10.0)
        if cell1.segment == 'OMCD':
            fvec[53] = cell1.conc[10,3]-cell1.conc[10,2]
        else:
            fvec[53] = ph[3]-pKNH3-np.log(abs(float(cell1.conc[9,3])/float(cell1.conc[10,3])))/np.log(10.0)
        fvec[54] = ph[4]-pKNH3-np.log(abs(float(cell1.conc[9,4])/float(cell1.conc[10,4])))/np.log(10.0)

    #---------------------------------------------------------------------
    #    For HCO2-/H2CO2
    #---------------------------------------------------------------------
        if cell1.segment != 'OMCD':
            fvec[60] = S[60]+S[65]
            fvec[61] = S[61]+S[66]
            fvec[62] = S[62]+S[67]
            fvec[63] = S[63]+S[68]
            fvec[64] = S[64]+S[69]
            fvec[65] = ph[0]-pKHCO2-np.log(abs(float(cell1.conc[12,0])/float(cell1.conc[13,0])))/np.log(10.0)
            fvec[69] = ph[4]-pKHCO2-np.log(abs(float(cell1.conc[12,4])/float(cell1.conc[13,4])))/np.log(10.0)

    #---------------------------------------------------------------------
    #    For pH
    #---------------------------------------------------------------------
        if cell1.segment == 'OMCD':
            fvec[55] = S[55]+S[50]-S[15]-S[30]
            fvec[56] = S[56]+S[51]-S[16]-S[31]
            fvec[57] = S[57]+S[52]-S[17]-S[32]
            fvec[58] = cell1.conc[11,3]-cell1.conc[11,2]
            fvec[59] = S[59]+S[54]-S[19]-S[34]
        else:
            fvec[55] = S[55]+S[50]-S[15]-S[30]-S[60]
            fvec[56] = S[56]+S[51]-S[16]-S[31]-S[61]
            fvec[57] = S[57]+S[52]-S[17]-S[32]-S[62]
            fvec[58] = S[58]+S[53]-S[18]-S[33]-S[63]
            fvec[59] = S[59]+S[54]-S[19]-S[34]-S[64]

    #---------------------------------------------------------------------
    #    For Volume
    #---------------------------------------------------------------------
        fvec[5*NS] = S[5*NS]
        fvec[5*NS+1] = S[5*NS+1]
        fvec[5*NS+2] = S[5*NS+2]
        if cell1.segment == 'OMCD':
            fvec[5*NS+3] = cell1.vol[3]-cell1.vol[2]
        else:
            fvec[5*NS+3] = S[5*NS+3]
        fvec[5*NS+4] = S[5*NS+4]
    #---------------------------------------------------------------------
    #	 For EP, need to satisfy electroneutrality
    #---------------------------------------------------------------------
        currM = 0
        if cell1.segment == 'OMCD':
            for j in range(NS):
                currM += zval[j]*(Jsol1[j,0,1]+Jsol1[j,0,2]+Jsol1[j,0,4])
        else:
            for j in range(NS):
                for k in range(1,5):
                    currM += zval[j]*Jsol1[j,0,k]
        fvec[5*NS+5] = currM

        volPrat = cell1.volref[1]/cell1.vol[1]
        volArat = cell1.volref[2]/cell1.vol[2]
        volBrat = cell1.volref[3]/cell1.vol[3]

        CimpP = cell1.cimpref[1]*volPrat
        CimpA = cell1.cimpref[2]*volArat
        CimpB = cell1.cimpref[3]*volBrat

        facP = np.exp(np.log(10.0)*(cell1.pH[1]-pKbuf))
        facA = np.exp(np.log(10.0)*(cell1.pH[2]-pKbuf))
        facB = np.exp(np.log(10.0)*(cell1.pH[3]-pKbuf))

        # these parameters
        #cPbuftot = 32.0
        #cAbuftot = 40.0
        #cBbuftot = 40.0

        #zPimp = -1.0
        #zAimp = -1.0
        #zBimp = -1.0

        CbufP = cPbuftot*volPrat*facP/(1+facP)
        CbufA = cAbuftot*volArat*facA/(1+facA)
        CbufB = cBbuftot*volBrat*facB/(1+facB)

        elecP = zPimp*CimpP-CbufP
        elecA = zAimp*CimpA-CbufA
        elecB = zBimp*CimpB-CbufB
        elecE = 0.0
        for j in range(NS):
            elecP += zval[j]*cell1.conc[j,1]
            elecA += zval[j]*cell1.conc[j,2]
            elecB += zval[j]*cell1.conc[j,3]
            elecE += zval[j]*cell1.conc[j,4]

        fvec[5*NS+6] = elecP
        fvec[5*NS+7] = elecA
        if cell1.segment == 'OMCD':
            fvec[5*NS+8] = cell1.ep[3]-cell1.ep[2]
        else:
            fvec[5*NS+8] = elecB
        fvec[5*NS+9] = elecE
    #---------------------------------------------------------------------
    #	 For Pressure, flow must be multiplied by Vref
    #---------------------------------------------------------------------
        if cell1.segment == 'CNT':
            ratio = 8.0*PI*visc/(Am**2)*coalesce*2
        elif cell1.segment == 'CCD' or cell1.segment == 'OMCD':
            ratio = 8.0*PI*visc/(Am**2)*coalesce
        fvec[5*NS+10] = cell1.pres[0]-cell0.pres[0]+ratio*cell1.vol[0]*Vref*cell1.len/cell1.total

        # for i in range(5*NS+11):
        # 	if fvec[i]<1.0e-5:
        # 		fvec[i]=0
        #print(cell1.pres[0],cell0.pres[0],ratio,Am,cell1.vol[0]*Vref,cell1.len)

    else:#if cell1.segment == 'SDL':

        Jvol1=np.zeros(NC*NC).reshape(NC,NC)
        Jsol1=np.zeros(NS*NC*NC).reshape(NS,NC,NC)
        ph = np.zeros(NC)

        cell1.conc[:,0] = x[0:NS]
        cell1.vol[0] = x[NS]
        cell1.pres[0] = x[NS+1]

        ph[0] = np.log(cell1.conc[11,0]/1000)/np.log(10)

        Jvol1,Jsol1 = flux.compute_fluxes(cell1,i)

        fvec = np.zeros(NS+3)
        S    = np.zeros(NS+3)

        Bm = PI*cell1.diam
        Am = PI*(cell1.diam**2)/4

        for i in range(NS):
            sumJsol1 = Jsol1[i,0,5]
            fsola = cell0.vol[0]*cell0.conc[i][0]*Vref/href
            fsolb = cell1.vol[0]*cell1.conc[i][0]*Vref/href
            fvec[i] = fsolb-fsola+Bm*cell1.len*sumJsol1/cell1.total

        fvec[3] = fvec[3]+fvec[4]+fvec[5]
        fvec[4] = ph[0] - pKHCO3 - np.log(cell1.conc[3,0]/cell1.conc[4,0])/np.log(10)
        fkin2 = cell1.dkh[0]*cell1.conc[5,0]-cell1.dkd[0]*cell1.conc[4,0]
        fvec[5] = fvec[5]+Am*cell1.len*fkin2/cell1.total/href

        fvec[6] = fvec[6]+fvec[7]
        fvec[7] = ph[0]-pKHPO4-np.log(cell1.conc[6,0]/cell1.conc[7,0])/np.log(10)

        fvec[9] = fvec[9]+fvec[10]
        fvec[10] = ph[0]-pKNH3-np.log(cell1.conc[9,0]/cell1.conc[10,0])/np.log(10)

        fvmult = Pfref*Vwbar*Cref
        sumJvb = Jvol1[0,5]*fvmult
        fvola = cell0.vol[0]*Vref
        fvolb = cell1.vol[0]*Vref
        fvec[NS] = fvolb-fvola+Bm*cell1.len*sumJvb/cell1.total

        ratio = 8*visc/(PI*(0.5*cell1.diam)**4)
        fvec[1+NS] = cell1.pres[0]-cell0.pres[0]+ratio*cell1.vol[0]*Vref*cell1.len/cell1.total

        fvec[2+NS] = sum(zval*cell1.conc[:,0])

    return fvec
#    return eqs







