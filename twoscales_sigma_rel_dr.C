
#include "TCanvas.h"
#include "TStyle.h"
#include "TH1.h"
#include "TGaxis.h"
#include "TRandom.h"

void twoscales_sigma_rel_dr()
{
   TCanvas *c1 = new TCanvas("c1","hists with different scales",600,400);
   c1->SetGrid();
   TMultiGraph *mg = new TMultiGraph();
//   mg->SetTitle("Exclusion graphs");

   //create/fill draw h1
   gStyle->SetOptStat(kFALSE);
   TFile *_file0 = TFile::Open("data/B1Z_evolution.root");
   auto gr1=(TGraphErrors*)_file0->Get("gZ20");
   mg->Add(gr1);
   TFile *file11 = TFile::Open("data/B1X_evolution.root");
   auto gr11=(TGraphErrors*)file11->Get("gZ20");
   mg->Add(gr11);
   mg->Draw("ap");
   auto yaxis = mg->GetYaxis();
   yaxis->SetRangeUser(-0.5,1);
   yaxis->SetTitle("#frac{(#sigma_{n}^{2} - #sigma_{0}^{2})^{1/2}}{#sigma_{0}}");
   yaxis->SetTitleOffset(1.0);
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

   //create hint1 filled with the bins integrap of h1
   TFile *file0 = TFile::Open("/home/ynisi/work/sk/monitor/dev/hv/out/sk5dr_shift.root");
   auto gr2=(TGraphErrors*)file0->Get("gdark_ave_wallUpBarrel");
   Float_t rightmax = 9.0;
   Float_t rightmin = 6.5;
   Float_t bias = gPad->GetUymax()-rightmax*(gPad->GetUymax()-gPad->GetUymin())/(rightmax-rightmin);
   Float_t scale = (gPad->GetUymax()-gPad->GetUymin())/(rightmax-rightmin);
   for (int i=0;i<gr2->GetN();i++) gr2->GetY()[i] = gr2->GetY()[i]*scale+bias;
   gr2->SetLineColor(kOrange);
   gr2->SetLineWidth(2);
   gr2->Draw("same");
   c1->Update();

   TLegend *legend = new TLegend(0.1,0.7,0.48,0.9);
   legend->AddEntry(gr1,"B1 collimator, Z, data","lep");
   legend->AddEntry(gr11,"B1 collimator, X, data","lep");
   legend->AddEntry(gr2,"Top wall ave. dark rate","l");
   legend->Draw();


   //draw an axis on the right side
   TGaxis *axis = new TGaxis(gPad->GetUxmax(),gPad->GetUymin(),
         gPad->GetUxmax(), gPad->GetUymax(),rightmin,rightmax,510,"+L");
   axis->SetLineColor(kRed);
   axis->SetLabelColor(kRed);
   axis->SetLabelOffset(0.0);
   axis->CenterTitle();
   axis->SetTitleColor(kRed);
   axis->SetTitle("Dark rate (kHz)");
   axis->Draw();

     TImage *img = TImage::Create();
   img->FromPad(c1);
   img->WriteImage("plots/SpotWidth_DarkNoise.png");
}
