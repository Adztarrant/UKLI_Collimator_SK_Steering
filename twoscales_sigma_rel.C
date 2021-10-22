
#include "TCanvas.h"
#include "TStyle.h"
#include "TH1.h"
#include "TGaxis.h"
#include "TRandom.h"

void twoscales_sigma_rel()
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
   xaxis->SetTimeFormat("%m-%d");
   xaxis->SetTimeOffset(0);
   xaxis->SetNdivisions(-219);
   xaxis->SetLimits(TDatime(2020, 7, 8, 0, 0, 0).Convert(), TDatime().Convert()+1209600);
   xaxis->SetLabelSize(0.025);
//   xaxis->CenterLabels();

/*   yaxis = gr11->GetYaxis();
   yaxis->SetRangeUser(-20,30);
   yaxis->SetTitleOffset(0.75);
   xaxis = gr11->GetXaxis();
   xaxis->SetLabelOffset(0.015);
   xaxis->SetTitleOffset(1.5);
   xaxis->SetTimeFormat("#splitline{%Y}{%m-%d}");
   xaxis->SetTimeOffset(0);
   xaxis->SetLabelSize(0.025);
   xaxis->CenterLabels();
*/
   c1->Update();

   //create hint1 filled with the bins integrap of h1
   TFile *file1 = TFile::Open("data/supply_bacteria.root");
   Float_t rightmax = 1500;
   Float_t rightmin = 0;
   Float_t bias = gPad->GetUymax()-rightmax*(gPad->GetUymax()-gPad->GetUymin())/(rightmax-rightmin);
   Float_t scale = (gPad->GetUymax()-gPad->GetUymin())/(rightmax-rightmin);
   auto gr3=(TGraphErrors*)file1->Get("Supply_0005");
   auto gr30=(TGraphErrors*)file1->Get("Supply_0507");
   for (int i=0;i<gr3->GetN();i++) gr3->GetY()[i] = gr3->GetY()[i]*scale+bias;
   for (int i=0;i<gr30->GetN();i++) gr30->GetY()[i] = gr30->GetY()[i]*scale+bias;
   gr3->SetMarkerColor(kViolet);
   gr3->SetMarkerSize(1.);
   gr3->SetLineColor(kViolet);
   gr3->SetLineWidth(1);
   gr3->SetMarkerStyle(1);
   gr3->Draw("P same");
   gr30->SetMarkerColor(kMagenta);
   gr30->SetMarkerSize(1.);
   gr30->SetLineColor(kMagenta);
   gr30->SetLineWidth(1);
   gr30->SetMarkerStyle(1);
   gr30->Draw("P same");

   TFile *file0 = TFile::Open("data/return_bacteria.root");
   auto gr2=(TGraphErrors*)file0->Get("Return_0005");
   auto gr20=(TGraphErrors*)file0->Get("Return_0507");
   for (int i=0;i<gr2->GetN();i++) gr2->GetY()[i] = gr2->GetY()[i]*scale+bias;
   for (int i=0;i<gr20->GetN();i++) gr20->GetY()[i] = gr20->GetY()[i]*scale+bias;
   gr20->SetMarkerColor(kRed);
   gr20->SetMarkerSize(1.);
   gr20->SetLineColor(kRed);
   gr20->SetLineWidth(1);
   gr20->SetMarkerStyle(1);
   gr20->Draw("P same");
   gr2->SetMarkerColor(kOrange);
   gr2->SetMarkerSize(1.);
   gr2->SetLineColor(kOrange);
   gr2->SetLineWidth(1);
   gr2->SetMarkerStyle(1);
   gr2->Draw("P same");
   c1->Update();

   TLegend *legend = new TLegend(0.1,0.7,0.48,0.9);
   legend->AddEntry(gr1,"B1 collimator, Z, data","lep");
   legend->AddEntry(gr11,"B1 collimator, X, data","lep");
   legend->AddEntry(gr2,"Return water count (0-0.5#mum)","l");
   legend->AddEntry(gr20,"Return water count (0.5-0.7#mum)","l");
   legend->AddEntry(gr3,"Supply water count (0-0.5#mum)","l");
   legend->AddEntry(gr30,"Supply water count (0.5-0.7#mum)","l");
   legend->Draw();


   //draw an axis on the right side
   TGaxis *axis = new TGaxis(gPad->GetUxmax(),gPad->GetUymin(),
   gPad->GetUxmax(), gPad->GetUymax(),0,rightmax,510,"+L");
   axis->SetLineColor(kRed);
   axis->SetLabelColor(kRed);
   axis->SetLabelOffset(0.0);
   axis->CenterTitle();
   axis->SetTitleColor(kRed);
   axis->SetTitle("Counts per 10 ml");
   axis->Draw();
      TImage *img = TImage::Create();
   img->FromPad(c1);
   img->WriteImage("plots/steering/SpotWidth.png");

}
