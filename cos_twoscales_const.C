
#include "TCanvas.h"
#include "TStyle.h"
#include "TH1.h"
#include "TGaxis.h"
#include "TRandom.h"

void cos_twoscales_const()
{
   TCanvas *c1 = new TCanvas("c1","hists with different scales",1800,1200);
   c1->SetGrid();
   TMultiGraph *mg = new TMultiGraph();
//   mg->SetTitle("Exclusion graphs");

   //create/fill draw h1
   gStyle->SetOptStat(kFALSE);
   TFile *_file0 = TFile::Open("data/B1COS_evolution.root");
   auto gr1=(TGraphErrors*)_file0->Get("gNGauss");
   mg->Add(gr1);
//   auto gr11=(TGraphErrors*)_file0->Get("gConst");
//  mg->Add(gr11);
  mg->Draw("ap");
   auto yaxis = mg->GetYaxis();
   int n=gr1->GetN();
   double masx = 1.25*TMath::MaxElement(n,gr1->GetY());
   double misn = 0.75*TMath::MinElement(n,gr1->GetY());
   yaxis->SetRangeUser(misn,masx);
   c1->Update();
   yaxis->SetTitle("N^{gauss}_{n}/N^{gauss}_{0}");
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
   xaxis->CenterLabels();

   c1->Update();

   TLegend *legend = new TLegend(0.1,0.7,0.48,0.9);
   legend->AddEntry(gr1,"B1 collimator data","lep");
//  legend->AddEntry(gr11,"B1 collimator data, C","lep");
   legend->Draw();

   TImage *img = TImage::Create();
   img->FromPad(c1);
   img->WriteImage("plots/const.png");
}
