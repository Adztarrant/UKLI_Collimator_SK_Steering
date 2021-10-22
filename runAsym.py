import ROOT
import numpy as np
import math
from array import array
import math
import argparse
import sys
import os
import analysisFuncs as F
import getConsts as Consts
import getPlots as Plots
import QTotalCalculationAndSubtractionMC as QCalcs
import MakeRegionNhitOverQPlots as CPlots
from listOfRuns import getListOfRuns1day

#import analyseFiles
### Get the input arguments from the command line at run time
parser = argparse.ArgumentParser()
parser.add_argument("period", type=int, nargs='?', default=0)
parser.add_argument("pos", type=int, nargs='?', default=1)
#parser.add_argument("wav", type=int, nargs='?', default=435)
#parser.add_argument("dir", type=str, nargs='?', default="/disk02/usr6/jmcelwee/monitoringData/backLog")
#parser.add_argument("fname", type=str, nargs='?', default="uklc1.082801.root")
parser.add_argument("--data", dest='data', default=False, action='store_true')
parser.add_argument("--test", dest='test', default=False, action='store_true')
parser.add_argument("--gaincor", dest='gaincor', default=False, action='store_true')
parser.add_argument("--hitcor", dest='hitcor', default=False, action='store_true')
parser.add_argument("--analyse", dest='analyse', default=False, action='store_true')
parser.add_argument("--makeTree", dest='makeTree', default=False, action='store_true')
parser.add_argument("--extraTree", dest='extraTree', default=False, action='store_true')
parser.add_argument("--UKInj", dest='UKInj', default=False, action='store_true')

#parser.add_argument("fname",type=str, nargs='?')
#args = parser.parse_args()
#infile = args.fname
#run_num = args.runno
#run_num = 00000
#injpos = args.pos
#injpos = 4
#wavelength = args.wav
#wavelength = 405
#directory = args.dir
#infile = args.fname

args = parser.parse_args()
#run_num = args.runno
#run numbers for each check period
#run_num = Consts.getListOfRuns5day(args.period) 
run_num = getListOfRuns1day(args.period) 
print(run_num)
injpos = args.pos
#wavelength = args.wav
wavelength = 435
directory = "/disk02/usr6/jmcelwee/monitoringData/backLog/"
#infile = args.fname


### Set data = True for data events, set test = True for SK4 test runs
#data            = False # Set to False to run in MC mode
#test            = True  # Set to True for runs in 'test' mode (ie no gain correction info available)
#gaincor         = False # Set to True for the gain corrections (charge/nhit) to be made
#hit_corrections = False # Set to True for diffuser hit corrections (solid angle, attenuation, path length)
#analyse         = True
#make_tree       = True
#extraTree       = False # Turn off saving vector info in Tree, which is very slow
## if test:
##     gain_run_num = 75604 # manually choose a recent run to use for gaincor if analysing test run
## else:
##     gain_run_num = run_num


### Arguments governing script control management
data      = args.data                   # Set data = True for data events, set test = True for SK4 test runs
data      = args.data                   # Set to False to run in MC mode
test      = args.test                   # Set to True for runs in 'test' mode for data (ie no gain correction info available)
gaincor   = args.gaincor                # Set to True for the gain corrections (charge/nhit) to be made
hitcor    = args.hitcor                 # Set to True for diffuser hit corrections (solid angle, attenuation, path length)
analyse   = args.analyse                # Produces the analysis histograms and hit/charge extra info (backgrounds etc) tree
makeTree  = args.makeTree               # Produces the basic tree containing total hits and total charge, with and without corrections
extraTree = args.extraTree              # Turn off saving vector info in Tree, which is very slow and makes large output files
UKInj     = args.UKInj                  # If True, UK injector locations will be used instead


t_cent = 750
timeshift = 0  # no timing shift in data
if not data:
    run_num = 1000
    timeshift = 60.0 # shift of timing in MC in ns
    t_cent = 800
#    print "INFO: Running in MC mode. Timing shift is +"+str(timeshift)

### Get the injector and target x,y,z coordinates for this position, and the speed of light in
### water for the selected wavelength
injXYZ, tarXYZ = Consts.getInjTarPos(injpos)
c = Consts.getSpeedOfLight(wavelength)

### If data, load the gain table and PMT production year tables (not needed for MC)
if data:
    #gain_cor = "/user2/pritchard/SuperK/SKDeploymentAnalysis/water.ave10.2"
    #prod_year_tab = "/user2/pritchard/SuperK/SKDeploymentAnalysis/pmt_prod_year.dat"
#    gain_cor = "/disk02/usr6/pablofer/calib/analysis/sk_ukli/water.ave10"
    gain_cor = "/home/ocon/waterjob/summary/water.ave10.2"
#    gain_cor = "water.ave10.2"
    prod_year_tab = "/disk02/usr6/pablofer/calib/analysis/sk_ukli/pmt_prod_year.dat"

    ### Load the relevant gain values and PMT production periods
    gain_vals = [0]*len(run_num)
    for i in range(len(run_num)):
        if (run_num[i]==85294):
            print 'hey'
            gain_vals[i] = F.GetGainVals(85293,gain_cor,test)
        elif (run_num[i]==85787):
            gain_vals[i] = F.GetGainVals(85786,gain_cor,test)
        elif (run_num[i]>86316):
            gain_vals[i] = F.GetGainVals(86316,gain_cor,test)
        elif (run_num[i]==85972 or run_num[i]==85975 or run_num[i]==85977):
            gain_vals[i] = F.GetGainVals(85974,gain_cor,test)
        else:
            gain_vals[i] = F.GetGainVals(run_num[i],gain_cor,test)

#    print(gain_vals[0])
    pmt_IDs,prod_years = F.LoadProdYear(prod_year_tab)

#################################################
# Open input root file, create output root file #
#################################################

if data:
    ifiledir = directory
#    ifile = [0]*len(run_num)
    tree = ROOT.TChain('tqtree')
    for i in run_num:
        ifile = 'uklc'+str(injpos-1)+'.0'+str(i)+'.root'
        datafile = ifiledir+ifile
        tree.AddFile(datafile)
        print('Added ', ifile)

else:
    ifiledir = directory
    ifile = infile

print(ifiledir)
print (ifile)

#datafile = ifiledir+ifile
#tree = ROOT.TChain('tqtree')
#tree.AddFile(datafile)
print(tree)
### Set up the output ROOT File
ofiledir = 'daily_col_plots/'
#Check if the output directory already exists, and make it if not
if not os.path.isdir(ofiledir):
    os.mkdir(ofiledir)
if data and args.period==0:
    ofilename = ofiledir+'20200709-20200713_B'+str(injpos-1)+'_Complete.root'
elif data and args.period>0:
    tree.GetEntry(1)
    if tree.year==120:
        yr=2020
    else:
        yr=2021
    date = yr*10000+tree.month*100+tree.day
    ofilename = ofiledir+str(date)+'_B'+str(injpos-1)+'_Complete.root'
else:
    ofilename = ofiledir+ifile[:-5]+'_Completed.root'
ofile = ROOT.TFile(ofilename,"RECREATE")

if makeTree:
###############################################################
# Set up the output TTree with the desired variables to store #
###############################################################
    
    VariableTree = ROOT.TTree("VariableTree","VariableTree")
    ### Values (ie one entry for every event)
    totalhits     = array('d',[0.0]) ; VariableTree.Branch("totalhits",totalhits,"totalhits/D",64000)
    totalhits_cor = array('d',[0.0]) ; VariableTree.Branch("totalhits_cor",totalhits_cor,"totalhits_cor/D",64000)
    totalQ        = array('d',[0.0]) ; VariableTree.Branch("totalQ",totalQ,"totalQ/D",64000)
    totalQ_cor    = array('d',[0.0]) ; VariableTree.Branch("totalQ_cor",totalQ_cor,"totalQ_cor/D",64000)
    if analyse:
        sumq_on       = array('d',[0.0]) ; VariableTree.Branch("sumq_on",sumq_on,"sumq_on/D",64000)
        sumq_dark     = array('d',[0.0]) ; VariableTree.Branch("sumq_dark",sumq_dark,"sumq_dark/D",64000)
        sumq_bgsub    = array('d',[0.0]) ; VariableTree.Branch("sumq_bgsub",sumq_bgsub,"sumq_bgsub/D",64000)
        nhit_on       = array('d',[0.0]) ; VariableTree.Branch("nhit_on",nhit_on,"nhit_on/D",64000)
        nhit_dark     = array('d',[0.0]) ; VariableTree.Branch("nhit_dark",nhit_dark,"nhit_dark/D",64000)
        nhit_sum      = array('d',[0.0]) ; VariableTree.Branch("nhit_sum",nhit_sum,"nhit_sum/D",64000)
        nhit_over_q   = array('d',[0.0]) ; VariableTree.Branch("nhit_over_q",nhit_over_q,"nhit_over_q/D",64000)
        
    ### Vectors (ie one entry for every hit)
    if extraTree:
        tof_target = ROOT.std.vector('double')()        ; VariableTree.Branch("tof_target",tof_target)
        tof_injector = ROOT.std.vector('double')()      ; VariableTree.Branch("tof_injector",tof_injector)
        Q = ROOT.std.vector('double')()                 ; VariableTree.Branch("Q",Q)
        Q_cor =  ROOT.std.vector('double')()            ; VariableTree.Branch("Q_cor",Q_cor)
        dist_target = ROOT.std.vector('double')()       ; VariableTree.Branch("dist_target",dist_target)
        dist_injector = ROOT.std.vector('double')()     ; VariableTree.Branch("dist_injector",dist_injector)
        prod_year = ROOT.std.vector('double')()         ; VariableTree.Branch("prod_year",prod_year)
        gain_applied = ROOT.std.vector('double')()      ; VariableTree.Branch("gain_applied",gain_applied)
        cable_num = ROOT.std.vector('double')()         ; VariableTree.Branch("cable_num",cable_num)
        hit_correction = ROOT.std.vector('double')()    ; VariableTree.Branch("hit_correction",hit_correction)
        hit_time = ROOT.std.vector('double')()          ; VariableTree.Branch("hit_time",hit_time)
        TCor_minus_TOFtar = ROOT.std.vector('double')() ; VariableTree.Branch("TCor_minus_TOFtar",TCor_minus_TOFtar)
        TCor_minus_TOFinj = ROOT.std.vector('double')() ; VariableTree.Branch("TCor_minus_TOFinj",TCor_minus_TOFinj)
        hit_angle = ROOT.std.vector('double')()         ; VariableTree.Branch("hit_angle",hit_angle)
        hit_x = ROOT.std.vector('double')()             ; VariableTree.Branch("hit_x",hit_x)
        hit_y = ROOT.std.vector('double')()             ; VariableTree.Branch("hit_y",hit_y)
        hit_z = ROOT.std.vector('double')()             ; VariableTree.Branch("hit_z",hit_z)
        z_diff = ROOT.std.vector('double')()            ; VariableTree.Branch("z_diff",z_diff)
        

###############

### Get all of the required histograms/graphs
### Check getPlots.py for the order in which plots are returned
TOFInjPlot, TOFTarPlot, TOFHaloPlot, QwBeamSpot, QwZPosBeam, QwZPosBeam_tOff, QwZPosBeam_tFocus, QwPosBeamY, QwPosBeamYbin, QwPosBeamY_monCorr, QwPosBeamYbin_monCorr, QwPosBeamX, QwPosBeamX_tOff, QwPosBeamX_tFocus, QwPosBeamXbin, QwPosBeamX_monCorr, QwPosBeamXbin_monCorr, QwPosBeamH, QwPosBeamH_tOff, QwPosBeamH_tFocus, QwAngBeam, QwCosAngBeam_tOff,QwCosAngBeamFront_tOff,QwCosAngBeamZoomFront_tOff,QwCosAngBeam_tFocus,QwCosAngBeamFront_tFocus,QwCosAngBeamZoomFront_tFocus, AngBeam, tvhits, ZTBAPlot, zposvTOF, Qw3DBeam, QinTank, QoutBeam, QinBeam, QinZRegion, QinZoutBeam = Plots.GetPlots(injpos-1)

### Start of event loop
nentries = tree.GetEntries()
#nentries = 100 # only use the first 100 events (much quicker). Uncomment above line for full sample
#nentries = 1000
#nentries = 1000

for i in range(nentries):
    if makeTree:
        nhits = 0
        nhits_cor = 0
        totQ = 0
        totQ_cor = 0
        if extraTree:
        ## clear the vectors so they can be refilled for the next event
            tof_target.clear()
            tof_injector.clear()
            Q.clear()
            Q_cor.clear()
            dist_target.clear()
            dist_injector.clear()
            prod_year.clear()
            gain_applied.clear()
            cable_num.clear()
            hit_correction.clear()
            TCor_minus_TOFtar.clear()
            TCor_minus_TOFinj.clear()
            hit_x.clear()
            hit_y.clear()
            hit_z.clear()
            z_diff.clear()

    tree.GetEntry(i) # get the next entry from the tree
    run = tree.run
    xhits = tree.pmtx_vec # all hits for one event are stored as a vector in the tree
    yhits = tree.pmty_vec
    zhits = tree.pmtz_vec
    times = tree.time_vec
    charges = tree.charge_vec # this vector stores the charge per hit
    mon_charge = tree.mon_charge_vec
    mon_cable = tree.mon_cable_vec
    PMTNums = tree.cable_vec
    hits = xhits.size() # find how many hits were in this event
    ### This is the main loop for all hits
    for imon in range(mon_charge.size()):
        if mon_cable[imon]==11256:
             qmon = mon_charge[imon]
    if i%200==0:
        print("Processed event number "+str(i)+". At run number "+str(run))
#    print("Monitor charge: "+str(qmon))
    qmon=1

    for h in range(hits):
        ### Get the x,y,z coordinates of the hit PMT
        hitXYZ = array('d',[])
        hitXYZ.append( xhits[h] )
        hitXYZ.append( yhits[h] )
        hitXYZ.append( zhits[h] )
        t = times[h]
        q = charges[h]
        
        ### If we are looking at data, perform the gain correction routine
        if data:
            PMT = PMTNums[h]
            production_year = prod_years[pmt_IDs.index(PMT)]
            run_index = run_num.index(run)
            gain = gain_vals[run_index][production_year]
            q_cor = q/(1+gain)
            nhit_cor = 1/(1+(gain*0.226))
        else:
            PMT = PMTNums[h]
            production_year = -1
            gain = 1
            q_cor = q
            nhit_cor = 1
            
        ### Calculate all necessary values
        TOF_inj, dist_inj = F.GetTimeOfFlight(injXYZ, hitXYZ, c)
        TOF_tar, dist_tar = F.GetTimeOfFlight(tarXYZ, hitXYZ, c)
        angRad = F.GetHitAngle(injXYZ, hitXYZ, tarXYZ, injpos)
        angDeg = math.degrees(angRad)
        xdiff = hitXYZ[0]-tarXYZ[0]
        ydiff = hitXYZ[1]-tarXYZ[1]
        zdiff = hitXYZ[2]-tarXYZ[2]
        xydiff = math.sqrt((xdiff*xdiff)+(ydiff*ydiff))

        z_sep = abs(hitXYZ[2]-injXYZ[2]) # separation in z between injector and hit PMT

        ### If the hit corrections will be applied, call them here
        if hitcor:
            rsqCor      = F.GetRSqCor(angRad)
            attCor      = F.GetAttCor(dist_inj, abs(injXYZ[2]-hitXYZ[2]))
            solidAngCor = F.GetSolidAngleCor(angRad)
        else:
            rsqCor      = 1
            attCor      = 1
            solidAngCor = 1
        totHitCor = rsqCor*attCor*solidAngCor*nhit_cor # calculate the corrected nhit
        t_cor_TOFinj = t-TOF_inj+timeshift
        t_cor_TOFtar = t-TOF_tar+timeshift
        
        ### Fill all of the plots
        # 1) charge weighted t-TOF(injector) for all events
        TOFInjPlot.Fill(t-TOF_inj+timeshift, q_cor)
        
        # 2) t-TOF(target) for all events outside of beam
        if dist_inj > 200 and dist_tar >320:
            TOFTarPlot.Fill(t-TOF_tar+timeshift, totHitCor)#, q_cor)
        if dist_inj > 200 and dist_tar >270:
            TOFHaloPlot.Fill(t-TOF_tar+timeshift, totHitCor)#, q_cor)

        # 3) 2D beam spot plot
        if dist_inj > 200 and abs((t-TOF_inj+timeshift)-t_cent)<50 and angDeg<80 and hitXYZ[2]<-1800:
            QwBeamSpot.Fill(hitXYZ[0],hitXYZ[1], totHitCor*q_cor)

        # 4) 1D beam spot plot (charge weighted z position) and angle        
        #if abs((t-TOF_inj+timeshift)-t_cent)<50 and dist_inj > 200 and angDeg<80:
        if dist_inj > 200: # basic injector exclusion for new test data
            if injpos in [2,3,4,5,6]:
                #if abs(ydiff) < 200:
                    QwZPosBeam.Fill(hitXYZ[2], totHitCor*q_cor)
                    if (t-TOF_inj+timeshift)>550 and (t-TOF_inj+timeshift)<850:
                        QwZPosBeam_tOff.Fill(hitXYZ[2], totHitCor*q_cor)
                    	QwCosAngBeam_tOff.Fill(math.cos(angRad), totHitCor*q_cor) 
                    	QwCosAngBeamFront_tOff.Fill(math.cos(angRad), totHitCor*q_cor)
                    	QwCosAngBeamZoomFront_tOff.Fill(math.cos(angRad), totHitCor*q_cor)
                    if (t-TOF_inj+timeshift)>950 and (t-TOF_inj+timeshift)<1250:
                        QwZPosBeam_tFocus.Fill(hitXYZ[2], totHitCor*q_cor)
                    	QwCosAngBeam_tFocus.Fill(math.cos(angRad), totHitCor*q_cor) 
                    	QwCosAngBeamFront_tFocus.Fill(math.cos(angRad), totHitCor*q_cor)
                    	QwCosAngBeamZoomFront_tFocus.Fill(math.cos(angRad), totHitCor*q_cor)
#                    if (t-TOF_inj+timeshift)>1200 and (t-TOF_inj+timeshift)<1350:
#                        QwZPosBeam_tDeepFocus.Fill(hitXYZ[2], totHitCor*q_cor)
                    if zdiff < 0: #if the target PMT position is above the hit PMT the angle between them will be negative
                        angDeg = -angDeg
                    QwAngBeam.Fill(angDeg, totHitCor*q_cor) 
#                    QwCosAngBeam.Fill(math.cos(angRad), totHitCor*q_cor) 
#                    QwCosAngBeamFront.Fill(math.cos(angRad), totHitCor*q_cor)
#                    QwCosAngBeamZoomFront.Fill(math.cos(angRad), totHitCor*q_cor)
                    AngBeam.Fill(angDeg, q_cor)
            else:#bottom or top injector
                #if abs(ydiff) < 50:
                    QwZPosBeam.Fill(hitXYZ[0], totHitCor*q_cor)
                    if xdiff < 0:#if the hit PMT is behind the target PMT in the x direction
                        angDeg = -angDeg
                    QwAngBeam.Fill(angDeg, totHitCor*q_cor)
#                    QwCosAngBeam.Fill(math.cos(angRad), totHitCor*q_cor)
#                    QwCosAngBeamFront.Fill(math.cos(angRad), totHitCor*q_cor)
#                    QwCosAngBeamZoomFront.Fill(math.cos(angRad), totHitCor*q_cor)
                    AngBeam.Fill(angDeg, q_cor)
         #4b 1D beam spot plot (y direction)
        if dist_inj > 200:
            if injpos in [2,3,4,5,6]:
                QwPosBeamY.Fill(hitXYZ[1], totHitCor*q_cor)
                QwPosBeamYbin.Fill(hitXYZ[1], totHitCor*q_cor)
                QwPosBeamY_monCorr.Fill(hitXYZ[1], totHitCor*q_cor/qmon)
                QwPosBeamYbin_monCorr.Fill(hitXYZ[1], totHitCor*q_cor/qmon)
        
        #4c 1D beam spot plot (x direction)
        if dist_inj > 200:
            if injpos in [2,3,4,5,6]:
                QwPosBeamX.Fill(hitXYZ[0], totHitCor*q_cor)
                QwPosBeamXbin.Fill(hitXYZ[0], totHitCor*q_cor)
                QwPosBeamX_monCorr.Fill(hitXYZ[0], totHitCor*q_cor/qmon)
                QwPosBeamXbin_monCorr.Fill(hitXYZ[0], totHitCor*q_cor/qmon)
                r2 = (hitXYZ[0]-injXYZ[0])**2 + (hitXYZ[1]-injXYZ[1])**2
                r20 = (tarXYZ[0]-injXYZ[0])**2 + (tarXYZ[1]-injXYZ[1])**2
                sign_r = np.sign(abs((hitXYZ[0]-injXYZ[0])/(hitXYZ[1]-injXYZ[1])) - abs((tarXYZ[0]-injXYZ[0])/(tarXYZ[1]-injXYZ[1])))
#                print r2,r20,r2-r20
                QwPosBeamH.Fill(sign_r * np.sqrt(abs(r2-r20)), totHitCor*q_cor)
                if (t-TOF_inj+timeshift)>550 and (t-TOF_inj+timeshift)<850:
                    QwPosBeamH_tOff.Fill(sign_r * np.sqrt(abs(r2-r20)), totHitCor*q_cor)
                    QwPosBeamX_tOff.Fill(hitXYZ[0], totHitCor*q_cor)
                if (t-TOF_inj+timeshift)>950 and (t-TOF_inj+timeshift)<1250:
                    QwPosBeamH_tFocus.Fill(sign_r * np.sqrt(abs(r2-r20)), totHitCor*q_cor)
                    QwPosBeamX_tFocus.Fill(hitXYZ[0], totHitCor*q_cor)
                
                # time vs hits in z-region
        if dist_inj > 200 and dist_tar > 320: # default region excludes <2m from injector and <3.2m from target centre                                                                                            
            if z_sep<280:
                tvhits.Fill(t, q_cor)

        # 5) t-TOF(tar) for hits in specific z region
        if dist_inj > 200 and dist_tar > 320: # default region excludes <2m from injector and <3.2m from target centre
            if z_sep <280:
                #ZTBAPlot.Fill(t-TOF_tar+timeshift), q_cor)
                ZTBAPlot.Fill(t-TOF_tar+timeshift, q_cor)
            
        # 5a) t-TOF(tar) against z-position of hit
        if dist_inj > 200:
            if injpos in [2,3,4,5,6]:
                zposvTOF.Fill(hitXYZ[2], t-TOF_tar+timeshift)

        # 6) Beam in 3d - NOT PROPERLY WORKING YET
        if dist_inj > 200 and abs((t-TOF_inj+timeshift)-t_cent)<5:
            Qw3DBeam.Fill(hitXYZ[0],hitXYZ[1],hitXYZ[2], totHitCor)

        # 7) Charge in tank but outside injector exclusion region
        if dist_inj > 200:
            QinTank.Fill(t-TOF_tar+timeshift, q_cor)
            # 8) Charge outside of the beam
            if dist_tar > 320:
                QoutBeam.Fill(t-TOF_tar+timeshift, q_cor)
            # 9) Charge inside the beam
            else:
                QinBeam.Fill(t-TOF_tar+timeshift, q_cor)
            # 10) Charge inside specific z band
            if z_sep < 280:
                QinZRegion.Fill(t-TOF_tar+timeshift, q_cor)
            # 11) Charge outside beam spot but in z band    
                if dist_tar > 320:
                    QinZoutBeam.Fill(t-TOF_tar+timeshift, q_cor)

        if makeTree and extraTree:
            ### Fill in the vector branches of the tree
            tof_target.push_back(TOF_tar)
            tof_injector.push_back(TOF_inj)
            Q.push_back(q)
            Q_cor.push_back(q_cor)
            dist_target.push_back(dist_tar)
            dist_injector.push_back(dist_inj)
            prod_year.push_back(production_year)
            gain_applied.push_back(gain)
            cable_num.push_back(PMT)
            hit_correction.push_back(totHitCor)
            TCor_minus_TOFtar.push_back(t_cor_TOFtar)
            TCor_minus_TOFinj.push_back(t_cor_TOFinj)
            hit_angle.push_back(angDeg)
            hit_x.push_back(hitXYZ[0])
            hit_y.push_back(hitXYZ[1])
            hit_z.push_back(hitXYZ[2])
            z_diff.push_back(zdiff)
        if makeTree:
            ### Increment the variable totals
            nhits += 1
            nhits_cor = nhits_cor + nhit_cor
            totQ = totQ + q
            totQ_cor = totQ_cor + q_cor

    if makeTree:
        totalhits[0] = nhits
        totalhits_cor[0] = nhits_cor
        totalQ[0] = totQ
        totalQ_cor[0] = totQ_cor

        VariableTree.Fill()

### Get the various analysis plots
if analyse:
    sumqo, sumqdark, sumq, nhito, darkhit, nhit, NhitOverQVal, hDataR, canNhit, canNhit1, can2, canP = CPlots.GetComparisonPlots(VariableTree, TOFInjPlot.Clone(), ZTBAPlot.Clone(), ZTBAPlot.Clone())
    if makeTree:
        sumq_on[0]       = sumqo
        sumq_dark[0]     = sumqdark
        sumq_bgsub[0]    = sumq
        nhit_on[0]       = nhito
        nhit_dark[0]     = darkhit
        nhit_sum[0]      = nhit
        nhit_over_q[0]   = NhitOverQVal
        VariableTree.Fill()

## Normalize by number of events
TOFInjPlot.Scale(1./nentries)
TOFTarPlot.Scale(1./nentries)
TOFHaloPlot.Scale(1./nentries)
QwBeamSpot.Scale(1./nentries)
QwZPosBeam.Scale(1./nentries)
QwZPosBeam_tOff.Scale(1./nentries)
QwZPosBeam_tFocus.Scale(1./nentries)
#QwZPosBeam_tDeepFocus.Scale(1./nentries)
QwPosBeamY.Scale(1./nentries)
QwPosBeamYbin.Scale(1./nentries)
QwPosBeamY_monCorr.Scale(1./nentries)
QwPosBeamYbin_monCorr.Scale(1./nentries)
QwPosBeamX.Scale(1./nentries)
QwPosBeamXbin.Scale(1./nentries)
QwPosBeamX_monCorr.Scale(1./nentries)
QwPosBeamXbin_monCorr.Scale(1./nentries)
QwPosBeamH.Scale(1./nentries)
QwPosBeamH_tOff.Scale(1./nentries)
QwPosBeamH_tFocus.Scale(1./nentries)
QwPosBeamX_tOff.Scale(1./nentries)
QwPosBeamX_tFocus.Scale(1./nentries)
QwAngBeam.Scale(1./nentries)
QwCosAngBeam_tOff.Scale(1./nentries)
QwCosAngBeamFront_tOff.Scale(1./nentries)
QwCosAngBeamZoomFront_tOff.Scale(1./nentries)
QwCosAngBeam_tFocus.Scale(1./nentries)
QwCosAngBeamFront_tFocus.Scale(1./nentries)
QwCosAngBeamZoomFront_tFocus.Scale(1./nentries)
AngBeam.Scale(1./nentries)
tvhits.Scale(1./nentries)
ZTBAPlot.Scale(1./nentries)
zposvTOF.Scale(1./nentries)
Qw3DBeam.Scale(1./nentries)
QinTank.Scale(1./nentries)
QoutBeam.Scale(1./nentries)
QinBeam.Scale(1./nentries)
QinZRegion.Scale(1./nentries)
QinZoutBeam.Scale(1./nentries)

### Write all of the histograms to the output root file
TOFInjPlot.Write()
TOFTarPlot.Write()
TOFHaloPlot.Write()
QwBeamSpot.Write()
QwZPosBeam.Write()
QwZPosBeam_tOff.Write()
QwZPosBeam_tFocus.Write()
#QwZPosBeam_tDeepFocus.Write()
QwPosBeamY.Write()
QwPosBeamYbin.Write()
QwPosBeamY_monCorr.Write()
QwPosBeamYbin_monCorr.Write()
QwPosBeamX.Write()
QwPosBeamH.Write()
QwPosBeamH_tOff.Write()
QwPosBeamH_tFocus.Write()
QwPosBeamX_tOff.Write()
QwPosBeamX_tFocus.Write()
QwPosBeamXbin.Write()
QwPosBeamX_monCorr.Write()
QwPosBeamXbin_monCorr.Write()
QwAngBeam.Write()
QwCosAngBeam_tOff.Write()
QwCosAngBeamFront_tOff.Write()
QwCosAngBeamZoomFront_tOff.Write()
QwCosAngBeam_tFocus.Write()
QwCosAngBeamFront_tFocus.Write()
QwCosAngBeamZoomFront_tFocus.Write()
AngBeam.Write()
tvhits.Write()
ZTBAPlot.Write()
zposvTOF.Write()
Qw3DBeam.Write()
QinTank.Write()
QoutBeam.Write()
QinBeam.Write()
QinZRegion.Write()
QinZoutBeam.Write()
if analyse:
    hDataR.SetName('ZTBAPlot_Norm')
    hDataR.Write()
    canNhit.Write()
    canNhit1.Write()
    can2.Write()
    canP.Write()
### Write the tree containing the variables to the output root file
if makeTree:
    VariableTree.Write('',ROOT.TObject.kOverwrite)  # Overwrite option needed in case file is large

print("Output written to "+ofilename)
ofile.Close()
