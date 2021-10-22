import ROOT
import math
from array import array

### Set timing windows for individual histograms
def GetTimingWindowsMC(hn,peak):
    if hn==97:
        onstart = peak-210
        onend = onstart+340
        offend = onstart
        offstart = offend-80
    elif hn==61:
        onstart = peak-210
        onend = onstart+340
        offend = onstart+220
        offstart = offend-80
    elif hn==62:
        onstart = peak-210
        onend = onstart+340
        offend = onstart+180 # changed from 70
        offstart = offend-80
    elif hn==63:
        onstart = peak-210
        onend = onstart+340
        offend = onstart+120 # changed from 1200
        offstart = offend-80
    elif hn==64:
        onstart = peak-210
        onend = onstart+340
        offend = onstart+70 # changed from 180
        offstart = offend-80 # changed from 130
    elif hn==65:
        onstart = peak-210
        onend = onstart+340
        offend = onstart+30  # changed from 220
        offstart = offend-80 #changed from 130
    elif hn==12:
        onstart = peak-70
        onend = onstart+500
        offend = onstart
        offstart = offend-80
    elif hn==72:
        onstart = peak-210
        onend = onstart+340
        offend = onstart
        offstart = offend-80
    elif hn==59:
        onstart = peak-210
        onend = onstart+340
    elif hn==13:
        onstart = peak-70
        onend = onstart+500
        offend = onstart
        offstart = offend-80
    else:
        print "ERROR: Invalid histogram number. Exiting"
        return 0;

    dw2 = 100
    dwp2 = 150

    on1=onstart+1; on2=onend
    hdark2=offend; hdark1=offstart+1
    qdark1=on2+dwp2+1; qdark2=qdark1+dw2-1
    
    return on1,on2,hdark1,hdark2,qdark1,qdark2

def SubtractDarkQ(hold,darkQ,darkwin):
    nbins = hold.GetNbinsX()
    vals = array('d',[])
    valErrs = array('d',[])
    maxT = hold.GetMaximumBin()
    binSize = hold.GetBinWidth(1)
    hName = hold.GetName()
    
    for i in range(nbins):
        vals.append(hold.GetBinContent(i))
        valErrs.append(hold.GetBinError(i))
    valsNew = array('d',[])
    for i in range(nbins):
        valsNew.append(vals[i]-darkQ*binSize/darkwin)
    hNew = hold.Clone()
    hNew.SetStats(0)
    hNew.SetMarkerStyle(8)
    hNew.SetMarkerSize(1)
    j=0
    for i in range(len(valsNew)):
        hNew.SetBinContent(i,valsNew[i])
        i+=1
    hNew.GetXaxis().SetRangeUser(0,2000)
    return hNew

def Rebin(hold, ngroup):
    xold = hold.GetXaxis()
    nbins = xold.GetNbins()
    xmin = xold.GetXmin()
    xmax = xold.GetXmax()
    if ngroup <= 0 or ngroup>nbins:
        print "Error in Rebin. Illegal value of ngroup"
        sys.exit(0)
    newbins = nbins/ngroup
    hnew = hold.Clone()
    #hnew.SetName('hNew')
    xnew = hnew.GetXaxis()
    xnew.Set(newbins,xmin,xmax)
    hnew.Set(newbins+2)

    b = 0
    i = 0
    oldbin = 1
    bincont = 0
    while b<=newbins:
        bincont = 0
        i = 0
        while i<ngroup:
            bincont+=hold.GetBinContent(oldbin+i)
            i+=1
        hnew.SetBinContent(b,bincont)
        oldbin+=ngroup
        b+=1

    return hnew

def GetQ(hist,hi):
    peak = int(hist.GetMaximumBin())
    #hi = int(hist.GetName()[-2:])
    on1,on2,hdark1,hdark2,qdark1,qdark2 = GetTimingWindowsMC(hi,peak)
    sumqo = float(hist.Integral(on1,on2))
    onwin = float(1+on2-on1)
    sumqdark = float(hist.Integral(hdark1,hdark2))
    darkwin = float(1+hdark2-hdark1)
    print "Dark window for Q = "+str(darkwin)+"ns"
    print "On window for Q = "+str(onwin)+"ns"    
    sumq = float(sumqo - ((onwin/darkwin)*sumqdark))
    return sumqo,sumqdark,sumq,onwin,darkwin

def GetHits(hist,peak,hi):
    #peak = int(hist.GetMaximumBin())
    #hi = int(hist.GetName()[-2:])
    sbin1,sbin2,dark1,dark2,qdark1,qdark2 = GetTimingWindowsMC(hi,peak)
    darkhit = float(hist.Integral(dark1,dark2))
    onwin = float(1+sbin2-sbin1)
    darkwin = float(1+dark2-dark1)
    if hi==72:
        nhito = float(hist.Integral(sbin1,sbin2))
        nhit = float(nhito - ((onwin*darkhit)/darkwin))
        return nhito,darkhit,nhit,onwin,darkwin
    else:
        return 0,darkhit,0,onwin,darkwin

def SubtractDarkHits(hold,darkHits,darkwin):
    nbins = hold.GetNbinsX()
    vals = array('d',[])
    valErrs = array('d',[])
    maxT = hold.GetMaximumBin()
    binSize = hold.GetBinWidth(1)
    hName = hold.GetName()
    darkwin = float(darkwin)
    
    for i in range(nbins):
        vals.append(hold.GetBinContent(i))
        valErrs.append(hold.GetBinError(i))
    valsNew = array('d',[])
    errsNew = array('d',[])
    for i in range(nbins):
        newVal = (vals[i])-darkHits*binSize/darkwin
        valsNew.append(newVal)
        errsNew.append(math.sqrt(newVal+10*darkHits/darkwin+darkHits*100/darkwin/darkwin))
    #print valsNew
    #print errsNew
    hNew = hold.Clone()
    hNew.SetStats(0)
    hNew.SetMarkerStyle(8)
    hNew.SetMarkerSize(1)
    j=0
    for i in range(len(valsNew)):
        hNew.SetBinContent(i,valsNew[i])
        hNew.SetBinError(i,errsNew[i])
        #i+=1
    hNew.GetXaxis().SetRangeUser(0,2000)
    return hNew

def ScaleByEvents(hold,events):
    nbins = hold.GetNbinsX()
    vals = array('d',[])
    valErrs = array('d',[])
    for i in range(nbins):
        vals.append(hold.GetBinContent(i))
        valErrs.append(hold.GetBinError(i))
    valsNew = array('d',[])
    valsErrNew = array('d',[])
    for i in range(nbins):
        valsNew.append(vals[i]/events)
        valsErrNew.append(valErrs[i]/events)
    hNew = hold.Clone()
    hNew.SetStats(0)
    hNew.SetMarkerStyle(8)
    hNew.SetMarkerSize(1)
    j=0
    for i in range(len(valsNew)):
        hNew.SetBinContent(i,valsNew[i])
        hNew.SetBinError(i,valsErrNew[i])
    hNew.GetXaxis().SetRangeUser(0,2000)
    return hNew
