import ROOT
from ROOT import TLatex
import argparse
import fileinput

def sedpy(infilename):
    infile = fileinput.input(infilename, inplace=True)
    header = 'Model'
    fail = 'FAIL'
    for line in infile:
        if header in line:
            for _ in range(32): # skip this line and next 4 lines
             next(infile, None)
        elif fail in line:
             next(infile, None)
        else:
            print line,
    fin = open(infilename, 'rt')
    data = fin.read()
    data = data.replace('/', '-')
    data = data.replace('\t', ' ')
    fin.close()
    fin = open(infilename, 'wt')
    fin.write(data)
    fin.close()

#    print('Done')



parser = argparse.ArgumentParser()
parser.add_argument('infilename', type=str, nargs='?', default='all_supply.tsv')
args = parser.parse_args()

inputFileName = args.infilename

sedpy(inputFileName)

if inputFileName == 'all_supply.tsv':
    g = ROOT.TGraphErrors()
    g.SetTitle("Bacteria count evolution in supply water")
    g1 = ROOT.TGraphErrors()
    g1.SetTitle("Bacteria count evolution in supply water")
elif inputFileName == 'all_return.tsv':
    g = ROOT.TGraphErrors()
    g.SetTitle("Bacteria count evolution in return water")
    g1 = ROOT.TGraphErrors()
    g1.SetTitle("Bacteria count evolution in return water")

lines = open(inputFileName, 'r').readlines()
for i, line in enumerate(lines):
    if i>-1:
        #print(i)
        date, time, total, small, medium, dummy, dummy, dummy, dummy = line.split()
        g.SetPoint(i, ROOT.TDatime("%s %s" %(date,time)).Convert(), float(medium))
        g1.SetPoint(i, ROOT.TDatime("%s %s" %(date,time)).Convert(), float(small))

if inputFileName == 'all_supply.tsv':
    ofile = ROOT.TFile("data/supply_bacteria.root","RECREATE")
    g.Write("Supply_0507")
    g1.Write("Supply_0005")
elif inputFileName == 'all_return.tsv':
    ofile = ROOT.TFile("data/return_bacteria.root","RECREATE")
    g.Write("Return_0507")
    g1.Write("Return_0005")

ofile.Close()

c = ROOT.TCanvas("c", "c", 950, 500)
g.Draw("3al")
yaxis = g.GetYaxis()
xaxis = g.GetYaxis()
yaxis.SetRangeUser(0,700)
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 9, 0, 0, 0).Convert(), ROOT.TDatime(2021, 2, 22, 0, 0, 0).Convert())
g1.Draw("3al same")
yaxis = g1.GetYaxis()
xaxis = g1.GetYaxis()
yaxis.SetRangeUser(0,700)
xaxis.SetLabelOffset(0.015)
xaxis.SetTitleOffset(1.5)
xaxis.SetTimeFormat("#splitline{%Y}{%m-%d}")
xaxis.SetTimeOffset(0)
xaxis.SetNdivisions(-219)
xaxis.SetLimits(ROOT.TDatime(2020, 7, 9, 0, 0, 0).Convert(), ROOT.TDatime(2021, 2, 22, 0, 0, 0).Convert())


if inputFileName == 'all_supply.tsv':
    c.Print("plots/Bacteria_supply.pdf","PDF")
elif inputFileName == 'all_return.tsv':
    c.Print("plots/Bacteria_return.pdf","PDF")

