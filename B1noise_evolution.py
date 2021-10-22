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
inputFileNameZ = "data/B%s_noise.txt" %col
 
# Create the time graph
gZ0 = ROOT.TGraphErrors()
gZ0.SetTitle("Variation of constant term in the vertical direction w.r.t. reference period (2020-07-09 to 2020-07-14);Date;A_{n}/A_{0}")

# Read the data and fill the graph with time along the X axis and number
# of users along the Y axis
 
linesZ = open(inputFileNameZ, "r").readlines()
h = '12:00:00'
j=0
error = 0.0
for i, line in enumerate(linesZ):
    if i==2:
        d, p00, ep00 = line.split()
#        print ROOT.TDatime("%s %s" %(d,h))
    if i>=2:
        d, p0, ep0 = line.split()
        gZ0.SetPoint(j, ROOT.TDatime("%s %s" %(d,h)).Convert()+259200, float(p0)/float(p00))
        error = 0.5*float(p0)/float(p00) * sqrt((float(ep0)/float(p0))**2+(float(ep00)/float(p00))**2)
        gZ0.SetPointError(j,0,error)
        j=j+1

# Draw the graphs
c = ROOT.TCanvas("c", "c", 950, 500)
c.SetLeftMargin(0.07)
c.SetRightMargin(0.04)
c.SetGrid()
gZ0.SetMarkerColor(ROOT.kBlue)
gZ0.SetMarkerSize(1)
gZ0.SetMarkerStyle(20)
gZ0.SetLineWidth(1)
gZ0.SetLineColor(ROOT.kBlue)
gZ0.Draw("AP")
gZ0.GetYaxis().CenterTitle()
# Make the X axis labelled with time
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
xaxis.SetLimits(ROOT.TDatime(2020, 7, 9, 0, 0, 0).Convert()+259200, ROOT.TDatime().Convert()+259200+1209600)
xaxis.SetLabelSize(0.025)
xaxis.CenterLabels()

outfile = ROOT.TFile("data/B1noise_evolution.root","recreate")
gZ0.Write("gZ0")
outfile.Close()


