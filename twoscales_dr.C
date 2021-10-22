/// \file
/// \ingroup tutorial_hist
/// \notebook
/// Example of macro illustrating how to superimpose two histograms
/// with different scales in the "same" pad.
///
/// \macro_image
/// \macro_code
///
/// \author Rene Brun

#include "TCanvas.h"
#include "TStyle.h"
#include "TH1.h"
#include "TGaxis.h"
#include "TRandom.h"

void twoscales_dr()
{
   TCanvas *c1 = new TCanvas("c1","hists with different scales",600,400);

   //create/fill draw h1
   gStyle->SetOptStat(kFALSE);
   TFile *_file0 = TFile::Open("data/B1noise_evolution.root");
   auto gr1=(TGraphErrors*)_file0->Get("gZ0");
   gr1->Draw("ap");
   auto yaxis = gr1->GetYaxis();
   yaxis->SetRangeUser(0.8,1.25);
   yaxis->SetTitleOffset(0.75);
   auto xaxis = gr1->GetXaxis();
   xaxis->SetLabelOffset(0.015);
   xaxis->SetTitleOffset(1.5);
   xaxis->SetTimeFormat("#splitline{%Y}{%m-%d}");
   xaxis->SetTimeOffset(0);
   xaxis->SetLabelSize(0.025);
   xaxis->CenterLabels();
   c1->Update();

   //create hint1 filled with the bins integral of h1
   TFile *file0 = TFile::Open("/home/ynisi/work/sk/monitor/dev/hv/out/sk5dr_shift.root");
   //auto gr2=(TGraphErrors*)file0->Get("gdark_ave_pdAllPMT");
   auto gr2=(TGraphErrors*)file0->Get("gdark_ave_wallUpBarrel");
   Float_t rightmax = 9.0;
   Float_t rightmin = 6.5;
   Float_t bias = gPad->GetUymax()-rightmax*(gPad->GetUymax()-gPad->GetUymin())/(rightmax-rightmin);
   Float_t scale = (gPad->GetUymax()-gPad->GetUymin())/(rightmax-rightmin);
   for (int i=0;i<gr2->GetN();i++) {
	   //cout << gr2->GetY()[i] << endl;
	   gr2->GetY()[i] = gr2->GetY()[i]*scale+bias;
	   cout << gr2->GetY()[i] << endl;
   }
   gr2->SetLineColor(kOrange);
   gr2->SetLineWidth(2);
   gr2->Draw("same");
   c1->Update();

   TLegend *legend = new TLegend(0.1,0.7,0.48,0.9);
   legend->AddEntry(gr1,"B1 collimator, Z, data","lac");
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
   img->WriteImage("plots/DarkNoise.png");
}
