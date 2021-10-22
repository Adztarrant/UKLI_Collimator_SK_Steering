
#include "TCanvas.h"
#include "TStyle.h"
#include "TH1.h"
#include "TGaxis.h"
#include "TRandom.h"

void twoscales_const()
{
   TCanvas *c1 = new TCanvas("c1","hists with different scales",600,400);
   c1->SetGrid();
   TMultiGraph *mg = new TMultiGraph();
//   mg->SetTitle("Exclusion graphs");

   //create/fill draw h1
   gStyle->SetOptStat(kFALSE);
   TFile *_file0 = TFile::Open("data/B1Z_evolution.root");
   auto gr1=(TGraphErrors*)_file0->Get("gZ1");
   mg->Add(gr1);
   TFile *file11 = TFile::Open("data/B1X_evolution.root");
   auto gr11=(TGraphErrors*)file11->Get("gZ1");
   mg->Add(gr11);
   mg->Draw("ap");
   auto yaxis = mg->GetYaxis();
   yaxis->SetRangeUser(0.7,1.3);
   yaxis->SetTitle("B_{n}/B_{0}");
   yaxis->SetTitleOffset(0.75);
   yaxis->CenterTitle();
   auto xaxis = mg->GetXaxis();
   xaxis->SetTimeDisplay(1);
   xaxis->SetTitle("Date");
   xaxis->CenterTitle();
   xaxis->SetLabelOffset(0.015);
   xaxis->SetTitleOffset(1.5);
   xaxis->SetTimeFormat("#splitline{%Y}{%m-%d}");
   xaxis->SetTimeOffset(0);
   xaxis->SetNdivisions(-219);
   xaxis->SetLimits(TDatime(2020, 7, 8, 0, 0, 0).Convert(), TDatime().Convert()+1209600);
   xaxis->SetLabelSize(0.025);

   c1->Update();

   TLegend *legend = new TLegend(0.1,0.7,0.48,0.9);
   legend->AddEntry(gr1,"B1 collimator, Z, data","lep");
   legend->AddEntry(gr11,"B1 collimator, X, data","lep");
   legend->Draw();
   TImage *img = TImage::Create();
   img->FromPad(c1);
   img->WriteImage("plots/steering/const.png");



}
