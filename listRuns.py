import ROOT
import numpy as np
import math
from array import array
import math
import argparse
import sys
import os
#import getConsts as Consts
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F
from ROOT import gROOT, gBenchmark, gRandom, gSystem
import ctypes


wavelength = 435
directory = '/disk02/usr6/jmcelwee/monitoringData/backLog/'
monthday = array('d',[0,31,59,90,120,151,181,212,243,273,304,334])


#################################################
# Open input root file, create output root file #
#################################################

#run_num = Consts.getAllRuns()
runs = np.array([])
count0=0
precount=0
startPeriod=330-1
startRun=85952
period=startPeriod

#runsFile = open('listOfRuns.py', 'w')
#print('from array import array', file=runsFile)
#print('import sys', file=runsFile)
#print('def getListOfRuns1day(period):', file=runsFile)
#print('    if period==0:', file=runsFile)
#print('        run = array(\'i\',[82909,82910,82911,82912,82914])', file=runsFile)
print('from array import array')
print('import sys')
print('def getListOfRuns1day(period):')
print('    if period==0:')
print('        run = array(\'i\',[82909,82910,82911,82912,82914])')
print('# Break in the run counting. Take into account this run-period relation for future intial conditions. If you need to analyze data in between ask Jordan or Pablo.')



for f in sorted(os.listdir(directory)):
    if f.endswith('.root') and f.startswith('uklc1.0'):
        fname = directory + f
        run = int(f[7:12])
#        print(f)
#        print(fname)
#        print(run)
        if run==85504: continue
        hfile = TFile(fname)
        tree = hfile.Get("tqtree")
        tree.GetEntry(2)
        run = tree.run
        year = tree.year
        month = tree.month
        day = tree.day
        if run==82909: # and run<=82914:
            count0 = day + monthday[month-1] + 365*year
        if run>=startRun:
            count  = day + monthday[month-1] + 365*year - count0
            if count%1==0 and count!=precount:
                if period>startPeriod:
                    print('    elif period=='+str(period)+':')
                    print '        run = array(\'i\',['+', '.join(map(str, runs))+'])'
                runs = np.array([run])
                period = period + 1
            else:
                runs = np.append(runs,run)
            precount=count
print('    else: print(\'Not a valid period\')')
print('    return run')

with open('last_period.txt', 'w') as f:
    f.write(str(period))
