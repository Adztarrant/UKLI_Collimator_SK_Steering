{
// Parameters for periods and collimators
FILE *fp = fopen("last_period.txt","r");
int ncols;
int period;
ncols = fscanf(fp,"%d",&period);
period=period+1;
cout << period << endl;
const int injpos = 2;

gStyle->SetOptFit(1111);
gStyle->SetOptFit(0);
gStyle->SetOptStat(0);
// Getting the files for each period
TFile *file[1000];
char filename[200];
int date;
int daysec=86400;
TDatime *dt[1000];
TDatime *dt0;
dt0 = new TDatime(2020,7,13,12,0,0);
for (int i=0; i<period; i++){
if (i==0) {
  dt[i] = new TDatime(2020,7,11,12,0,0);
  date = dt[i]->GetYear() *10000 + dt[i]->GetMonth() *100 + dt[i]->GetDay();
  sprintf(filename,"daily_col_plots/20200709-20200713_B%d_Complete.root",injpos);
}
else {
  dt[i] = new TDatime(dt0->Convert()+i*daysec);
  date = dt[i]->GetYear() *10000 + dt[i]->GetMonth() *100 + dt[i]->GetDay();
  sprintf(filename,"daily_col_plots/%d_B%d_Complete.root",date,injpos);
}
  file[i] = TFile::Open(filename,"read");
        cout << i << " " << date << endl;
}

// Getting the histograms for each period
TH1F *hist_off[1000];
TH1F *hist_on[1000];
for (int i=0; i<period; i++){
	file[i]->cd();
//        cout << i << " " << date << endl;
       	hist_off[i] = (TH1F*) QwCosAngBeamFront_tOff->Clone();
	hist_on[i]  = (TH1F*) QwCosAngBeamFront_tFocus->Clone();
//	file[i]->Delete();
}

TF1 *f0 = new TF1("f0","[0]",0.85,1.0);
TF1 *fexp = new TF1("fexp","[1]*exp([2]*(x-1))",0.85,1.0);
TF1 *fgauss = new TF1("fgauss","[4]*exp(-0.5*pow(((x-[6])/[5]),2))",0.85,1.0);
TF1 *fh = new TF1("fh","f0+fexp+fgauss",0.85,1.0);
fh->SetParLimits(0,0,1.5);
fh->SetParLimits(1,-100,100.0);
fh->SetParLimits(2,10,100);
fh->SetParLimits(3,10,200);
fh->SetParLimits(4,5e-4,5e-3);
fh->SetParLimits(5,0.99,1.0);

TF1 *fz = new TF1("fz", "([0])",0.85,1.0);
fz->SetParLimits(0,0,10);

// Plot formatting
hist_off[0]->SetLineWidth(2);
hist_off[0]->SetLineColor(1);
hist_on[0]->SetLineWidth(2);
hist_on[0]->SetLineColor(1);
for (int i=1; i<period; i++){
	hist_off[i]->SetLineWidth(2);
	hist_off[i]->SetLineColor(1);
	hist_on[i]->Add(hist_off[i],-1);
	hist_on[i]->SetLineWidth(2);
	hist_on[i]->SetLineColor(1);
}

ofstream outon;
char fouton[200];
sprintf(fouton,"data/B%d_COS.txt",injpos);
outon.open(fouton);
outon << "Year  Month  Day  Noise  Noise_error  Const.  C_error  NExp  NExp_error  Slope  Slope_error  Norm  N_error  Sigma  S_error  Pos.  P_error " << endl;
outon << "----------------------------------" << endl;

TLegend *left;
TLegend *left1;
for (int i=0; i<period; i++){
	hist_on[i]->Draw("hist");
	hist_on[i]->GetYaxis()->SetRangeUser(0.05,200.);
	hist_on[i]->Fit("fh","M I R Q");
	fh->Draw("same");
	f0->SetParameter(0,fh->GetParameter(0));
	fexp->SetParameter(1,fh->GetParameter(1));
	fexp->SetParameter(2,fh->GetParameter(2));
	fgauss->SetParameter(3,fh->GetParameter(3));
	fgauss->SetParameter(4,fh->GetParameter(4));
	fgauss->SetParameter(5,fh->GetParameter(5));
	f0->Draw("same");
	f0->SetLineColor(kBlue);
	fexp->Draw("same");
	fexp->SetLineColor(kGreen);
	fgauss->Draw("same");
	fgauss->SetLineColor(kCyan);
	if (i==0){
		left = new TLegend(0.1,0.55,0.45,0.9);
		left->AddEntry("fh","Fitting function","l");
		left->AddEntry("f0","Baseline of fitting function","l");
		left->AddEntry("fexp","Exponential part of fitting function","l");
		left->AddEntry("fgauss","Gaussian part of fitting function","l");
	}
	left->Draw("same");
	c1->Update();
	c1->SetLogy();
//  	if (i==0) c1->SaveAs("gplots.pdf(");
//  	else if (i==period-1) c1->SaveAs("gplots.pdf)");
//        else c1->SaveAs("gplots.pdf");
	hist_off[i]->Draw("hist");
	hist_off[i]->Fit("fz","M I R Q");
	fz->Draw("same");
	fz->SetLineColor(kViolet);
	if (i==0){
		left1 = new TLegend(0.1,0.55,0.45,0.9);
		left1->AddEntry("fz","Noise par. (baseline outside signal time window)","l");
	}
	left1->Draw("same");
	outon << dt[i]->GetYear() << "-" << dt[i]->GetMonth() << "-" << dt[i]->GetDay() << " " << fz->GetParameter(0) << " " << fz->GetParError(0) << " " << fh->GetParameter(0) << " " << fh->GetParError(0) << " " << fh->GetParameter(1) << " " << fh->GetParError(1) << " " << fh->GetParameter(2) << " " << fh->GetParError(2) << " " << " " << fh->GetParameter(3) << " " << fh->GetParError(4) << " " << fh->GetParameter(4) << " " << fh->GetParError(4) << " "<< fh->GetParameter(5) << " " << fh->GetParError(5) << endl;
	
	c1->Update();
//	if (i==n_periods-1) c1->SaveAs("gplots.pdf)");
//        else c1->SaveAs("gplots.pdf");
}

outon.close();
}
