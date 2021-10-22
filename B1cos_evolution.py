#include "TCanvas.h"
#include "TStyle.h"
#include "TH1.h"
#include "TGaxis.h"
#include "TRandom.h"

import ROOT
from ROOT import TLatex
from ROOT import gROOT, gPad
from math import sqrt, acos
from numpy import sign

 
# Open the data file. This csv contains the usage statistics of a CERN IT
# service, SWAN, during two weeks. We would like to plot this data with
# ROOT to draw some conclusions from it.
col = 1
inputFileNameZ = "data/B%s_COS.txt" %col
#inputFileNameZ = "B5_COS.txt"
 
# Create the time graph
gNoise = ROOT.TGraphErrors()
gNoise.SetTitle("Variation of noise (dark rate) term w.r.t. reference period (2020-07-09 to 2020-07-14);Date;Noise_{n}/Noise_{0}")
gConst = ROOT.TGraphErrors()
gConst.SetTitle("Variation of constant term w.r.t. reference period (2020-07-09 to 2020-07-14);Date;C_{n}/C_{0}")
gNexp = ROOT.TGraphErrors()
gNexp.SetTitle("Variation of exp. normalization term w.r.t. reference period (2020-07-09 to 2020-07-14);Date; N^{exp}_{n}/N^{exp}_{0}")
gSlope = ROOT.TGraphErrors()
gSlope.SetTitle("Variation of slope term w.r.t. reference period (2020-07-09 to 2020-07-14);Date;k_{n}/k_{0}")
gNSlope = ROOT.TGraphErrors()
gNSlope.SetTitle("Variation of N/k w.r.t. reference period (2020-07-09 to 2020-07-14);Date;(N_{n}/k_{n})/(N_{0}/k_{0})")
gNGauss = ROOT.TGraphErrors()
gNGauss.SetTitle("Variation of Gaussian nomalization w.r.t. reference period (2020-07-09 to 2020-07-14);Date;N_{n}^{Gauss}/N_{0}^{Gauss}")
gGSigma = ROOT.TGraphErrors()
gGSigma.SetTitle("Variation of the width of spot w.r.t. reference period (2020-07-09 to 2020-07-14);Date;(#sigma_{n}^{2} - #sigma_{0}^{2})^{1/2} / #sigma_{0}")
gSpot = ROOT.TGraphErrors()
gSpot.SetTitle("Variation of spot angular position w.r.t. reference period (2020-07-09 to 2020-07-14);Date;#theta^{Gauss}_{n} - #theta^{Gauss}_{0} (rad)")

# Read the data and fill the graph with time along the X axis and number
# of users along the Y axis
 
linesZ = open(inputFileNameZ, "r").readlines()
h = '12:00:00'
j=0
error = 0.0
dummy = 0.0
for i, line in enumerate(linesZ):
    if i==2:
        d, noise0, enoise0, const0, econst0, nexp0, enexp0, slope0, eslope0, ngauss0, engauss0, sigma0, esigma0, pos0, epos0 = line.split()
#        print ROOT.TDatime("%s %s" %(d,h))
    if i>=2:
        d, noise, enoise, const, econst, nexp, enexp, slope, eslope, ngauss, engauss, sigma, esigma, pos, epos = line.split()

        gNoise.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert(), float(noise)/float(noise0))
        error = float(noise)/float(noise0) * sqrt((float(enoise)/float(noise))**2+(float(enoise0)/float(noise0))**2)
        gNoise.SetPointError(j,0,error)

#        gConst.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert(), float(const))
#        gConst.SetPointError(j,0,float(econst))
        gConst.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert(), float(const)/float(const0))
        if float(const)==0:
            error = float(const)/float(const0) * sqrt((float(econst0)/float(const0))**2)
        else:
            error = float(const)/float(const0) * sqrt((float(econst)/float(const))**2+(float(econst0)/float(const0))**2)

        gConst.SetPointError(j,0,error)

        dummy = sign(float(sigma)-float(sigma0))*sqrt(abs(float(sigma)**2-float(sigma0)**2))
        gGSigma.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert(), dummy/float(sigma0))
        if i==2:
            error = abs(dummy)/float(sigma0) * sqrt((float(esigma)+float(esigma0))**2/(float(sigma)+float(sigma0))**2 + float(esigma0)**2/float(sigma0)**2)
        else:
            if dummy==0:
                error = (float(sigma)*float(esigma))
            else:
                error = (float(sigma)*float(esigma)+float(sigma0)*float(esigma0))/abs(dummy**2)
                error = abs(dummy)/float(sigma0) * sqrt(error**2 + float(esigma0)**2/float(sigma0)**2)
        gGSigma.SetPointError(j,0,error)

        gNexp.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert(), float(nexp)/float(nexp0))
        error = float(nexp)/float(nexp0) * sqrt((float(enexp)/float(nexp))**2+(float(enexp0)/float(nexp0))**2)
        gNexp.SetPointError(j,0,error)

        gSlope.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert(), float(slope)/float(slope0))
        error = float(slope)/float(slope0) * sqrt((float(eslope)/float(slope))**2+(float(eslope0)/float(slope0))**2)
        gSlope.SetPointError(j,0,error)

        gNSlope.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert(), float(nexp)/float(slope)/(float(nexp0)/float(slope0)))
        error = float(nexp)/float(slope)/(float(nexp0)/float(slope0)) * sqrt((float(enexp)/float(nexp))**2+(float(enexp0)/float(nexp0))**2+(float(eslope)/float(slope))**2+(float(eslope0)/float(slope0))**2)
        gNSlope.SetPointError(j,0,error)

        gNGauss.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert(), float(ngauss)/float(ngauss0)*float(sigma)/float(sigma0))
        error = float(ngauss)/float(ngauss0) *float(sigma)/float(sigma0)* sqrt((float(engauss)/float(ngauss))**2+(float(engauss0)/float(ngauss0))**2+(float(esigma0)/float(sigma0))**2+(float(esigma)/float(sigma))**2)
        gNGauss.SetPointError(j,0,error)

        gSpot.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert(), acos(float(pos))-acos(float(pos0)))
        ep=float(pos)+float(epos)
        ep0=float(pos0)+float(epos0)
        if ep>1:
            ep=1
        if ep0>1:
            ep0=1
        error = sqrt((acos(float(pos0)-acos(ep0)))**2+(acos(float(pos)-acos(ep)))**2)
        gSpot.SetPointError(j,0,error)

        j=j+1

# Draw the graphs
c = ROOT.TCanvas("c", "c", 950, 500)
c.SetLeftMargin(0.07)
c.SetRightMargin(0.04)
c.SetGrid()
gNoise.SetMarkerColor(ROOT.kBlue)
gNoise.SetMarkerStyle(20)
gNoise.SetMarkerSize(1)
gNoise.SetLineWidth(1)
gNoise.SetLineColor(ROOT.kBlue)
gNoise.Draw("ap")
gNoise.GetYaxis().CenterTitle()
yaxis = gNoise.GetYaxis()
yaxis.SetRangeUser(0.7,1.3)
xaxis = gNoise.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
#xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert(), ROOT.TDatime().Convert()+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gConst.SetMarkerColor(ROOT.kBlue)
gConst.SetMarkerStyle(20)
gConst.SetLineWidth(1)
gConst.SetLineColor(ROOT.kBlue)
gConst.Draw("AP")
gConst.GetYaxis().CenterTitle()
yaxis = gConst.GetYaxis()
yaxis.SetRangeUser(0.7,1.3)
xaxis = gConst.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
#xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert(), ROOT.TDatime().Convert()+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gSlope.SetMarkerColor(ROOT.kBlue)
gSlope.SetMarkerStyle(20)
gSlope.SetLineWidth(1)
gSlope.SetLineColor(ROOT.kBlue)
gSlope.Draw("ap")
gSlope.GetYaxis().CenterTitle()
yaxis = gSlope.GetYaxis()
yaxis.SetRangeUser(0.8,1.5)
yaxis.SetTitleOffset(0.75)
xaxis = gSlope.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
#xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert(), ROOT.TDatime().Convert()+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gNSlope.SetMarkerColor(ROOT.kBlue)
gNSlope.SetMarkerStyle(20)
gNSlope.SetLineWidth(1)
gNSlope.SetLineColor(ROOT.kBlue)
gNSlope.Draw("ap")
gNSlope.GetYaxis().CenterTitle()
yaxis = gNSlope.GetYaxis()
yaxis.SetRangeUser(0.8,1.5)
yaxis.SetTitleOffset(0.75)
xaxis = gNSlope.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
#xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert(), ROOT.TDatime().Convert()+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gNexp.SetMarkerColor(ROOT.kBlue)
gNexp.SetMarkerStyle(20)
gNexp.SetLineWidth(1)
gNexp.SetLineColor(ROOT.kBlue)
gNexp.Draw("AP")
gNexp.GetYaxis().CenterTitle()
yaxis = gNexp.GetYaxis()
yaxis.SetRangeUser(0.8,1.5)
yaxis.SetTitleOffset(0.75)
xaxis = gNexp.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
#xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert(), ROOT.TDatime().Convert()+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gNGauss.SetMarkerColor(ROOT.kBlue)
gNGauss.SetMarkerStyle(20)
gNGauss.SetLineWidth(1)
gNGauss.SetLineColor(ROOT.kBlue)
gNGauss.Draw("AP")
gNGauss.GetYaxis().CenterTitle()
yaxis = gNGauss.GetYaxis()
yaxis.SetRangeUser(0.7,1.3)
yaxis.SetTitleOffset(0.75)
xaxis = gNGauss.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
#xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert(), ROOT.TDatime().Convert()+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gGSigma.SetMarkerColor(ROOT.kBlue)
gGSigma.SetMarkerStyle(20)
gGSigma.SetLineWidth(1)
gGSigma.SetLineColor(ROOT.kBlue)
gGSigma.Draw("AP")
gGSigma.GetYaxis().CenterTitle()
yaxis = gGSigma.GetYaxis()
yaxis.SetRangeUser(-0.5,1.0)
yaxis.SetTitleOffset(0.75)
xaxis = gGSigma.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
#xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert(), ROOT.TDatime().Convert()+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

gSpot.SetMarkerColor(ROOT.kBlue)
gSpot.SetMarkerStyle(20)
gSpot.SetLineWidth(1)
gSpot.SetLineColor(ROOT.kBlue)
gSpot.Draw("AP")
gSpot.GetYaxis().CenterTitle()
yaxis = gSpot.GetYaxis()
yaxis.SetRangeUser(-0.2,0.2)
yaxis.SetTitleOffset(0.75)
xaxis = gSpot.GetXaxis()
xaxis.SetTimeDisplay(1)
xaxis.CenterTitle()
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
#xaxis.SetLimits(ROOT.TDatime(2020, 7, 8, 0, 0, 0).Convert(), ROOT.TDatime().Convert()+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

outfile = ROOT.TFile("data/B1COS_evolution.root","recreate")
gNoise.Write("gNoise")
gConst.Write("gConst")
gSlope.Write("gSlope")
gNSlope.Write("gNSlope")
gNexp.Write("gNexp")
gNGauss.Write("gNGauss")
gGSigma.Write("gGSigma")
gSpot.Write("gSpot")
outfile.Close()


