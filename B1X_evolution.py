#include "TCanvas.h"
#include "TStyle.h"
#include "TH1.h"
#include "TGaxis.h"
#include "TRandom.h"

import ROOT
from ROOT import TLatex
from ROOT import gROOT, gPad
from math import sqrt
from numpy import sign

 
# Open the data file. This csv contains the usage statistics of a CERN IT
# service, SWAN, during two weeks. We would like to plot this data with
# ROOT to draw some conclusions from it.
col = 1
inputFileNameZ = "data/B%s_X.txt" %col
 
# Create the time graph
gZ0 = ROOT.TGraphErrors()
gZ0.SetTitle("Variation of constant term in the vertical direction w.r.t. reference period (2020-07-09 to 2020-07-14);Date;A_{n}/A_{0}")
gZ1 = ROOT.TGraphErrors()
gZ1.SetTitle("Variation of normalization term in the vertical direction w.r.t. reference period (2020-07-09 to 2020-07-14);Date;B_{n}/B_{0}")
gZ20 = ROOT.TGraphErrors()
gZ20.SetTitle("Variation of spot width term in the vertical direction w.r.t. reference period (2020-07-09 to 2020-07-14);Date;(#sigma_{n}^{2} - #sigma_{0}^{2})^{1/2} / #sigma_{0}")
gZ2 = ROOT.TGraphErrors()
gZ2.SetTitle("Variation of spot width term in the vertical direction w.r.t. reference period (2020-07-09 to 2020-07-14);Date;(#sigma_{n}^{2} - #sigma_{0}^{2})^{1/2} (cm)")
gZstd = ROOT.TGraphErrors()
gZstd.SetTitle("Variation of spot width term in the vertical direction w.r.t. reference period (2020-07-09 to 2020-07-14);Date;(#sigma_{n}^{2} - #sigma_{0}^{2})^{1/2} (cm)")
gbact = ROOT.TGraphErrors()
gbact.SetTitle("Variation of the estimated concentration of bacteria inside SK tank;Date;#n_{bacteria}^{coll}")
gbactstd = ROOT.TGraphErrors()
gbactstd.SetTitle("Variation of the estimated concentration of bacteria inside SK tank;Date;#n_{bacteria}^{coll}")
gZ3 = ROOT.TGraphErrors()
gZ3.SetTitle("Variation of spot position term in the vertical direction w.r.t. reference period (2020-07-09 to 2020-07-14);Date;#mu_{n} - #mu_{0} (cm)")
gZmean = ROOT.TGraphErrors()
gZmean.SetTitle("Variation of spot position term in the vertical direction w.r.t. reference period (2020-07-09 to 2020-07-14);Date;#mu_{n} - #mu_{0} (cm)")

# Read the data and fill the graph with time along the X axis and number
# of users along the Y axis
 
linesZ = open(inputFileNameZ, "r").readlines()
h = '12:00:00'
j=0
error = 0.0
dummy = 0.0
for i, line in enumerate(linesZ):
    if i==2:
        d, p00, ep00, p10, ep10, p20, ep20, p30, ep30, s0, es0, m0, em0 = line.split()
#        print ROOT.TDatime("%s %s" %(d,h))
    if i>=2:
        d, p0, ep0, p1, ep1, p2, ep2, p3, ep3, s, es, m, em = line.split()
        gZ0.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert()+259200, float(p0)/float(p00))
        error = float(p0)/float(p00) * sqrt((float(ep0)/float(p0))**2+(float(ep00)/float(p00))**2)
        gZ0.SetPointError(j,0,error)
        gZ1.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert()+259200, float(p1)/float(p10)*float(p2)/float(p20))
        error = float(p1)/float(p10) *float(p2)/float(p20)* sqrt((float(ep1)/float(p1))**2+(float(ep10)/float(p10))**2+(float(ep20)/float(p20))**2+(float(ep2)/float(p2))**2)
        gZ1.SetPointError(j,0,error)

        dummy = sign(float(p2)-float(p20))*sqrt(abs(float(p2)**2-float(p20)**2))
        gZ20.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert()+259200, dummy/float(p20))
        gZ2.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert()+259200, dummy)
        gbact.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert()+259200, dummy**2/1.231**2)
        if i==2:
            error = abs(dummy)/float(p20) * sqrt((float(ep2)+float(ep20))**2/(float(p2)+float(p20))**2 + float(ep20)**2/float(p20)**2)
        else:
            error = (float(p2)*float(ep2)+float(p20)*float(ep20))/abs(dummy**2)
            error = abs(dummy)/float(p20) * sqrt(error**2 + float(ep20)**2/float(p20)**2)

        gZ20.SetPointError(j,0,error)
        if i==2:
            error = (float(ep2)+float(ep20))
        else:
            error = abs(dummy) * (float(p2)*float(ep2)+float(p20)*float(ep20))/abs(dummy**2)
        gZ2.SetPointError(j,0,error)
        if i==2:
            error = sqrt(error**2+0.02**2)
        else:
            error = 2*dummy**2/1.231**2 * sqrt(error**2/dummy**2+0.02**2/1.231**2)
        gbact.SetPointError(j,0,error)

        dummy = sign(float(s)-float(s0))*sqrt(abs(float(s)**2-float(s0)**2))
        gZstd.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert()+259200, dummy)
        gbactstd.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert()+259200, dummy**2/1.231**2)
        if i==2:
            error = (float(es)+float(es0))
        else:
            error = abs(dummy) * (float(s)*float(es)+float(s0)*float(es0))/abs(dummy**2)
        gZstd.SetPointError(j,0,error)
        if i==2:
            error = sqrt(error**2+0.02**2)
        else:
            error = 2*dummy**2/1.231**2 * sqrt(error**2/dummy**2+0.02**2/1.231**2)
        gbactstd.SetPointError(j,0,error)

        gZ3.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert()+259200, float(p3)-float(p30))
        error = sqrt(float(ep30)**2+float(ep3)**2)
        gZ3.SetPointError(j,0,error)
        gZmean.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert()+259200, float(m)-float(m0))
        error = sqrt(float(em0)**2+float(em)**2)
        gZmean.SetPointError(j,0,error)
        j=j+1

# Draw the graphs
c = ROOT.TCanvas("c", "c", 950, 500)
c.SetLeftMargin(0.07)
c.SetRightMargin(0.04)
c.SetGrid()
gZ0.SetMarkerColor(ROOT.kGreen)
gZ0.SetMarkerSize(1)
gZ0.SetLineWidth(1)
gZ0.SetLineColor(ROOT.kGreen)
gZ0.Draw("ep")
gZ0.GetYaxis().CenterTitle()
yaxis = gZ0.GetYaxis()
yaxis.SetRangeUser(0.5,1.5)
xaxis = gZ0.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gZ1.SetMarkerColor(ROOT.kGreen)
gZ1.SetMarkerStyle(20)
gZ1.SetLineWidth(1)
gZ1.SetLineColor(ROOT.kGreen)
gZ1.Draw("AP")
gZ1.GetYaxis().CenterTitle()
yaxis = gZ1.GetYaxis()
yaxis.SetRangeUser(0.7,1.3)
xaxis = gZ1.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gZ2.SetMarkerColor(ROOT.kGreen)
gZ2.SetMarkerStyle(20)
gZ2.SetLineWidth(1)
gZ2.SetLineColor(ROOT.kGreen)
gZ2.Draw("ep")
gZ2.GetYaxis().CenterTitle()
yaxis = gZ2.GetYaxis()
yaxis.SetRangeUser(-50,50)
yaxis.SetTitleOffset(0.75)
xaxis = gZ2.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gZstd.SetMarkerColor(ROOT.kGreen)
gZstd.SetMarkerStyle(20)
gZstd.SetLineWidth(1)
gZstd.SetLineColor(ROOT.kGreen)
gZstd.Draw("ep")
gZstd.GetYaxis().CenterTitle()
yaxis = gZstd.GetYaxis()
yaxis.SetRangeUser(-50,50)
yaxis.SetTitleOffset(0.75)
xaxis = gZstd.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gZ20.SetMarkerColor(ROOT.kGreen)
gZ20.SetMarkerStyle(20)
gZ20.SetLineWidth(1)
gZ20.SetLineColor(ROOT.kGreen)
gZ20.Draw("AP")
gZ20.GetYaxis().CenterTitle()
yaxis = gZ20.GetYaxis()
yaxis.SetRangeUser(-0.25,0.75)
yaxis.SetTitleOffset(0.75)
xaxis = gZ20.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gbact.SetMarkerColor(ROOT.kGreen)
gbact.SetMarkerStyle(20)
gbact.SetLineWidth(1)
gbact.SetLineColor(ROOT.kGreen)
gbact.Draw("AP")
gbact.GetYaxis().CenterTitle()
yaxis = gbact.GetYaxis()
yaxis.SetRangeUser(0,800)
yaxis.SetTitleOffset(0.75)
xaxis = gbact.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gbactstd.SetMarkerColor(ROOT.kGreen)
gbactstd.SetMarkerStyle(20)
gbactstd.SetLineWidth(1)
gbactstd.SetLineColor(ROOT.kGreen)
gbactstd.Draw("AP")
gbactstd.GetYaxis().CenterTitle()
yaxis = gbactstd.GetYaxis()
yaxis.SetRangeUser(0,800)
yaxis.SetTitleOffset(0.75)
xaxis = gbactstd.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gZ3.SetMarkerColor(ROOT.kGreen)
gZ3.SetMarkerStyle(20)
gZ3.SetLineWidth(1)
gZ3.SetLineColor(ROOT.kGreen)
gZ3.Draw("AP")
gZ3.GetYaxis().CenterTitle()
yaxis = gZ3.GetYaxis()
yaxis.SetRangeUser(-2,2)
yaxis.SetTitleOffset(0.75)
xaxis = gZ3.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gZmean.SetMarkerColor(ROOT.kGreen)
gZmean.SetMarkerStyle(20)
gZmean.SetLineWidth(1)
gZmean.SetLineColor(ROOT.kGreen)
gZmean.Draw("AP")
gZmean.GetYaxis().CenterTitle()
yaxis = gZmean.GetYaxis()
yaxis.SetRangeUser(-2,2)
yaxis.SetTitleOffset(0.75)
xaxis = gZmean.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

outfile = ROOT.TFile("data/B1X_evolution.root","recreate")
gZ0.Write("gZ0")
gZ1.Write("gZ1")
gZ2.Write("gZ2")
gZstd.Write("gZstd")
gZ20.Write("gZ20")
gbact.Write("gbact")
gbactstd.Write("gbactstd")
gZ3.Write("gZ3")
gZmean.Write("gZmean")
outfile.Close()

