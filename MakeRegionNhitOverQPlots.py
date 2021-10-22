import ROOT
import sys
from array import array
import QTotalCalculationAndSubtractionMC as QCalcs

### Function for shifting values in an array
def shift(key, array):
    return array[key % len(array):] + array[:key % len(array)]

### Function to shift peak time of histogram to a reference time
def ShiftTiming(hold,refT,maxT):
    nbins = hold.GetNbinsX()
    binWidth = hold.GetBinWidth(1)
    vals = array('d',[])
    valErrs = array('d',[])
    hold.GetXaxis().SetRangeUser(0,900)
    #maxT = hold.GetMaximumBin()
        
    hName = hold.GetName()
    #hNameNew = hName+Type
    
    for i in range(nbins):
        vals.append(hold.GetBinContent(i))
        valErrs.append(hold.GetBinError(i))
        
    shiftT = maxT-refT
    valsShifted = shift(shiftT,vals)
    hNew = hold.Clone()
    hNew.SetStats(0)
    hNew.SetMarkerStyle(8)
    hNew.SetMarkerSize(1)
    j=0
    for i in range(len(valsShifted)):
        hNew.SetBinContent(i,valsShifted[i])
        i+=1
    hNew.GetXaxis().SetRangeUser(0,2000)
    return hNew
    
### Start of main script

def GetComparisonPlots(treeData, QTotPlot, ScatHitRegionPlot, ZRegionPlot):
    
    entries = float(treeData.GetEntries())
    print "Total events = "+str(entries)
    ### First step is to extract the total charge, dark charge, background subtracted charge
    hist = QTotPlot

    ### Set the global peak time using this histogram
    peakT = hist.GetMaximumBin()
    print "The peak time to be used is "+str(peakT)+"ns, taken from histogram 12"
    hnum_qtot = 12
    refT = 590 # reference time to correct peak to

    hDataNew = ShiftTiming(hist,refT,peakT) # shift the timing by the average of the meantime plot
    sumqo,sumqdark,sumq,onwin,darkwin = QCalcs.GetQ(hDataNew,hnum_qtot) # get the charge information

    ### First plot: Qw events vs Tcor-TOFinj, with background included
    can2 = ROOT.TCanvas('can2','can2',1200,700)
    hDataNew.SetStats(0)
    hDataNew.SetMarkerStyle(8)
    hDataNew.SetMarkerSize(0.7)
    hDataNew.SetLineColor(1)
    hDataNew.SetMarkerColor(1)
    hDataNew.GetYaxis().SetLabelSize(0.06)
    hDataNew.SetTitle('Tcor-TOF(from injector) for Total PMTs')
    hDataNew.GetXaxis().SetTitle('Tcor-TOFinj (ns)')
    hDataNew.GetXaxis().SetTitleOffset(1.3)
    hDataNew.GetYaxis().SetTitle('Qw events/4ns')
    hDataNew.GetYaxis().SetTitleOffset(1.8)
    hDataNew.GetXaxis().SetLabelSize(0.05) # New to change axis label size
    hDataNew.GetYaxis().SetLabelSize(0.05)
    hDataNew.SetMaximum(hDataNew.GetMaximum()*1.1)
    hDataNew.SetMinimum(-100)
    hDataNewA = QCalcs.Rebin(hDataNew,10)
    hDataNewA.GetXaxis().SetRangeUser(0,1400)
    hDataNewA.Draw('E1')
    ### Second plot: Same as first with dark charge subtracted (plotted on same)
    hDataNewB = hDataNewA.Clone()
    hDataNewB = QCalcs.SubtractDarkQ(hDataNewB,sumqdark,darkwin)
    hDataNewB.SetLineColor(2)
    hDataNewB.SetStats(0)
    hDataNewB.SetMarkerStyle(8)
    hDataNewB.SetMarkerSize(0.7)
    hDataNewB.SetMarkerColor(2)
    hDataNewB.SetLineColor(2)
    hDataNewB.SetMinimum(0)
    Qintegral = float(hDataNewB.Integral(0,2000))
    print Qintegral
    print hDataNewB.GetEntries()
    hDataNewB.SetMinimum(-100)
    hDataNewB.Draw('E1same')
    legendQ = ROOT.TLegend(0.59,0.67,0.88,0.87)
    legendQ.SetFillStyle(1001)
    legendQ.SetFillColor(0)
    legendQ.SetLineColor(1)
    legendQ.SetLineStyle(1)
    legendQ.AddEntry(hDataNew, 'Before dark charge subtraction')
    legendQ.AddEntry(hDataNewB,'After dark charge subtraction')
    legendQ.Draw()

    print "Total charge = "+str(sumqo)+" p.e."
    print "Dark charge = "+str(sumqdark)+" p.e."
    print "Sum charge after dark subtraction = "+str(sumq)+" p.e."
    print "Total background subtracted charge integral = "+str(Qintegral)+" p.e."
    ### Third plot: charge per event vs Tcor-TOFinj, with dark and signal regions highlighted
    canP = ROOT.TCanvas('canP','canP',1200,700)
    on1,on2,hdark1,hdark2,qdark1,qdark2 = QCalcs.GetTimingWindowsMC(hnum_qtot,refT) # Timing already shifted previously
    scaleF=entries
    ### Create 3 new histograms which are clones of the original
    hDataScaled = hDataNew.Clone()
    hDataOn = hDataScaled.Clone()
    hDataDark = hDataScaled.Clone()
    hDataScaled.Sumw2()
    hDataScaled.Scale(1/scaleF)
    hDataScaled.SetTitle('Tcor-TOF(from injector) for Total PMTs')
    hDataScaled.GetXaxis().SetTitle('Tcor-TOFinj (ns)')
    hDataScaled.GetXaxis().SetTitleOffset(1.3)
    hDataScaled.GetYaxis().SetTitle('P.E. per event')
    hDataScaled.GetYaxis().SetTitleOffset(1.4)
    hDataScaled.Draw('E1')
    hDataScaled.GetXaxis().SetRangeUser(hdark1,on2)
    hDataDark.Scale(1/scaleF)
    hDataDark.GetXaxis().SetRangeUser(hdark1,hdark2)
    hDataDark.SetLineColor(2)
    hDataDark.SetLineWidth(2)
    hDataDark.Draw('same')
    hDataOn.Scale(1/scaleF)
    hDataOn.SetLineWidth(2)
    hDataOn.GetXaxis().SetRangeUser(on1,on2)
    hDataOn.SetLineColor(3)
    hDataOn.Draw('same')
    legend = ROOT.TLegend(0.59,0.67,0.88,0.87)
    legend.SetFillStyle(1001)
    legend.SetFillColor(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.AddEntry(hDataOn, 'Signal Q region '+str(on1)+'ns to '+str(on2)+'ns')
    legend.AddEntry(hDataDark,'Dark Q region, '+str(hdark1)+'ns to '+str(hdark2)+'ns')
    legend.Draw()
    ### Next step is to calculate the hits in the scattered region, 2-10m from the injector
    histH = ScatHitRegionPlot
    hnum_nhit = 97
    hDataNhit = ShiftTiming(histH,refT,peakT) # Shift the timing of the plot
    nhito,darkhit,nhit,onwin,darkwin = QCalcs.GetHits(hDataNhit,refT, hnum_nhit)

    print "Total hits = "+str(nhito)
    print "Dark hits = "+str(darkhit)
    print "Sum hits with dark rate subtracted = "+str(nhit)

    ### Fourth plot: hits vs Tcor-TOFtar in scattered hit region, with background included
    canNhit1 = ROOT.TCanvas('canNhit1','canNhit1',1200,700)
    hDataNhit.SetStats(0)
    hDataNhit.SetMarkerStyle(8)
    hDataNhit.SetMarkerSize(0.7)
    hDataNhit.SetLineColor(1)
    hDataNhit.SetMarkerColor(1)
    hDataNhit.GetYaxis().SetLabelSize(0.06)
    hDataNhit.SetTitle('Tcor-TOF(from injector) for Total PMTs')
    hDataNhit.GetXaxis().SetTitle('Tcor-TOFinj (ns)')
    hDataNhit.GetXaxis().SetTitleOffset(1.3)
    hDataNhit.GetYaxis().SetTitle('Events/4ns')
    hDataNhit.GetYaxis().SetTitleOffset(1.8)
    hDataNhit.GetXaxis().SetLabelSize(0.05)
    hDataNhit.GetYaxis().SetLabelSize(0.05)
    hDataNhit.SetMinimum(-100)
    hDataNhitA = QCalcs.Rebin(hDataNhit,10)
    hDataNhitA.SetMaximum(hDataNhitA.GetMaximum()*1.1)
    hDataNhitA.GetXaxis().SetRangeUser(0,1400)
    hDataNhitA.Draw('E1')
    canNhit1.Update()

    ### Fifth plot: hits vs Tcor-TOFtar in scattered hit region, with background subtracted, plotted on same as #3
    hDataNhitB = hDataNhitA.Clone()
    hDataNhitB = QCalcs.SubtractDarkHits(hDataNhitB,darkhit,darkwin)
    hDataNhitB.SetLineColor(2)
    hDataNhitB.SetStats(0)
    hDataNhitB.SetMarkerStyle(8)
    hDataNhitB.SetMarkerSize(0.7)
    hDataNhitB.SetMarkerColor(2)
    hDataNhitB.SetLineColor(2)
    hDataNhitB.Draw('E1same')
    legendH = ROOT.TLegend(0.59,0.67,0.88,0.87)
    legendH.SetFillStyle(1001)
    legendH.SetFillColor(0)
    legendH.SetLineColor(1)
    legendH.SetLineStyle(1)
    legendH.AddEntry(hDataNhit, 'Before dark hit subtraction')
    legendH.AddEntry(hDataNhitB,'After dark hit subtraction')
    legendH.Draw()

    ### Sixth plot: hits per event in scattered region vs Tcor-TOFtar
    canNhit = ROOT.TCanvas('canNhit','canNhit',1200,700)
    on1,on2,hdark1,hdark2,qdark1,qdark2 = QCalcs.GetTimingWindowsMC(hnum_nhit,refT) # Timing already shifted previously
    scaleF = entries
    hDataNhitScaled = hDataNhit.Clone()
    hDataNhitDark = hDataNhitScaled.Clone()
    hDataNhitOn = hDataNhitScaled.Clone()
    hDataNhitScaled.Sumw2()
    hDataNhitScaled.Scale(1/scaleF)
    hDataNhitScaled.SetTitle('Tcor-TOF(from target) for scattered hit region')
    hDataNhitScaled.GetXaxis().SetTitle('Tcor-TOFtar (ns)')
    hDataNhitScaled.GetXaxis().SetTitleOffset(1.3)
    hDataNhitScaled.GetYaxis().SetTitle('Hits per event')
    hDataNhitScaled.GetYaxis().SetTitleOffset(1.4)
    hDataNhitScaled.Draw('P')
    hDataNhitScaled.GetXaxis().SetRangeUser(hdark1-100,on2+300)
    
    hDataNhitDark.Scale(1/scaleF)
    hDataNhitDark.GetXaxis().SetRangeUser(hdark1,hdark2)
    hDataNhitDark.SetLineColor(2)
    hDataNhitDark.SetLineWidth(2)
    hDataNhitDark.Draw('same')
    
    hDataNhitOn.Scale(1/scaleF)
    hDataNhitOn.SetLineWidth(2)
    hDataNhitOn.GetXaxis().SetRangeUser(on1,on2)
    hDataNhitOn.SetLineColor(3)
    hDataNhitOn.Draw('same')
    legendNew = ROOT.TLegend(0.14,0.71,0.46,0.86)
    legendNew.SetFillStyle(1001)
    legendNew.SetFillColor(0)
    legendNew.SetLineColor(1)
    legendNew.SetLineStyle(1)
    legendNew.AddEntry(hDataNhitOn, 'Signal Nhit region '+str(on1)+'ns to '+str(on2)+'ns')
    legendNew.AddEntry(hDataNhitDark,'Dark Nhit region, '+str(hdark1)+'ns to '+str(hdark2)+'ns')
    legendNew.Draw()
    
    Qtot = sumq
    NhitScat = nhit
    NhitOverQVal = nhit/sumq

    print "Nhit/Q for scattered hit region = "+str(NhitOverQVal)

    # Another histogram for barrel region specific histogram
    h97 = ZRegionPlot

    canHists = ROOT.TCanvas('canHists','canHists',1200,700)
    newBinWidth = 10
    hDataR = ShiftTiming(h97,refT,peakT)
    hn = 97
    on1R,on2R,hdark1R,hdark2R,qdark1R,qdark2R = QCalcs.GetTimingWindowsMC(hn,refT)
    nhitoR,darkhitR,nhitR,onwinR,darkwinR = QCalcs.GetHits(hDataR,refT,hn)
    hDataR = QCalcs.Rebin(hDataR,newBinWidth)
    hDataR = QCalcs.SubtractDarkHits(hDataR,darkhitR,darkwinR)
    hDataR.GetXaxis().SetRangeUser(hdark1R,1000)
    hDataR.Scale(1/(Qtot))
    hDataR.GetYaxis().SetTitle('Nhit/Q (/'+str(newBinWidth)+'ns)')
    hDataR.GetXaxis().SetTitle('Tcor-TOF(target) (ns)')
    hDataR.SetStats(0)
    hDataR.SetMarkerStyle(8)
    hDataR.SetMarkerSize(0.7)
    hDataR.SetLineColor(1)
    hDataR.SetMarkerColor(1)
    hDataR.GetYaxis().SetLabelSize(0.06)
    hDataR.SetTitle('Tcor-TOF(from injector) for z dependence region')
    hDataR.GetXaxis().SetTitleOffset(1.3)
    hDataR.GetYaxis().SetTitleOffset(1.8)
    hDataR.GetXaxis().SetLabelSize(0.05) # New to change axis label size
    hDataR.GetYaxis().SetLabelSize(0.05)
    hDataR.GetXaxis().SetRangeUser(100,1200)
    #hDataR.SetMaximum(1200)
    #hDataR.SetMinimum(-100)
    #hDataR.Draw('E1')

    return sumqo, sumqdark, sumq, nhito, darkhit, nhit, NhitOverQVal, hDataR, canNhit, canNhit1, can2, canP
