{
// Parameters for periods and collimators
FILE *fp = fopen("last_period.txt","r");
int ncols;
int period;
ncols = fscanf(fp,"%d",&period);
period=period+1;
cout << period << endl;
const int injpos = 1;

gStyle->SetOptFit(1111);
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
  cout << i << " " << date << endl;
  file[i] = TFile::Open(filename,"read");
}

// Getting the histograms for each period
TH1F *histz[1000];
TH1F *histx[1000];
for (int i=0; i<period; i++){
	file[i]->cd();
       	histz[i] = (TH1F*) QwZPosBeam_tFocus->Clone();
//	histz[i]->Scale(1/histz[i]->Integral());
	histx[i] = (TH1F*) QwPosBeamX_tFocus->Clone();
//	histx[i]->Scale(1/histx[i]->Integral());
//	file[i]->Delete();
}


//f1->SetParLimits(1,10,400);
//f1->SetParLimits(2,1,2);
//f1->SetParLimits(3,-1650,-1450);

TF1 *fh = new TF1("fh", "([0]+[1]*exp(-0.5*pow(((x-[3])/[2]),2)))",-1650.,-1000.);
fh->SetParLimits(0,0,10);
fh->SetParLimits(1,10,400);
fh->SetParLimits(2,5,400);
fh->SetParLimits(3,-1650,-1550);

TF1 *fz = new TF1("fz", "([0]+[1]*exp(-0.5*pow(((x-[3])/[2]),2)))",700.,1700.);
//TF1 *fz = new TF1("fz", "([0]+[1]*exp(-0.5*pow(((x-[3])/[2]),2)))",400.,900.);
//TF1 *fz = new TF1("fz", "([0]+[1]*exp(-0.5*pow(((x-[3])/[2]),2)))",-500.,100.);
fz->SetParLimits(0,0,10);
fz->SetParLimits(1,10,400);
fz->SetParLimits(2,20,400);

if (injpos==1) fz->SetParLimits(3,1100,1300);
else if (injpos==2){
 fz->SetParLimits(3,700,900);
}
else if (injpos==3) fz->SetParLimits(3,-300,-100);
else if (injpos==4) fz->SetParLimits(3,-850,-650);
else if (injpos==5) fz->SetParLimits(3,-1550,-1300);

// Plot formatting
histz[0]->SetLineWidth(2);
histz[0]->SetLineColor(1);
histx[0]->SetLineWidth(2);
histx[0]->SetLineColor(1);
for (int i=1; i<period; i++){
	histz[i]->SetLineWidth(2);
	histz[i]->SetLineColor(2);
	histx[i]->SetLineWidth(2);
	histx[i]->SetLineColor(2);
}

ofstream outx;
ofstream outz;
char foutx[200],foutz[200];
sprintf(foutx,"data/B%d_X.txt",injpos);
sprintf(foutz,"data/B%d_Z.txt",injpos);
outx.open(foutx);
outz.open(foutz);
outx << "Year  Month  Day  Const.  C_error  Norm.  N_error  Sigma  S_error  Pos.  P_error   StdDev   Std_error   Mean   Mean_error" << endl;
outx << "----------------------------------" << endl;
outz << "Year  Month  Day  Const.  C_error  Norm.  N_error  Sigma  S_error  Pos.  P_error   StdDev   Std_error   Mean   Mean_error" << endl;
outz << "----------------------------------" << endl;

for (int i=0; i<period; i++){
	histx[i]->Draw("hist");
//cout << "hey" << endl;
	histx[i]->Fit("fh","M I R Q");
	fh->Draw("same");
	histx[i]->GetXaxis()->SetRangeUser(-1660.,-1540.);
	outx << dt[i]->GetYear() << "-" << dt[i]->GetMonth() << "-" << dt[i]->GetDay() << " " << fh->GetParameter(0) << " " << fh->GetParError(0) << " " << fh->GetParameter(1) << " " << fh->GetParError(1) << " " << fh->GetParameter(2) << " " << fh->GetParError(2) << " " << fh->GetParameter(3) << " " << fh->GetParError(3) << " " << histx[i]->GetStdDev() << " " << histx[i]->GetStdDevError() << " " << histx[i]->GetMean() << " " << histx[i]->GetMeanError() << endl;
//	legx[i]->Draw();
	c1->Update();
//  	if (i==0) c1->SaveAs("gplots.pdf(");
//        else c1->SaveAs("gplots.pdf");
	histz[i]->Draw("hist");
	histz[i]->Fit("fz","M I R Q");
	fz->Draw("same");
	histz[i]->GetXaxis()->SetRangeUser(1075.,1325.);
	outz << dt[i]->GetYear() << "-" << dt[i]->GetMonth() << "-" << dt[i]->GetDay() << " " << fz->GetParameter(0) << " " << fz->GetParError(0) << " " << fz->GetParameter(1) << " " << fz->GetParError(1) << " " << fz->GetParameter(2) << " " << fz->GetParError(2) << " " << fz->GetParameter(3) << " " << fz->GetParError(3) << " " << histz[i]->GetStdDev() << " " << histz[i]->GetStdDevError() << " " << histz[i]->GetMean() << " " << histz[i]->GetMeanError() << endl;
//	legz[i]->Draw();
	c1->Update();
//	if (i==period-1) c1->SaveAs("gplots.pdf)");
//	else c1->SaveAs("gplots.pdf");
}

outx.close();
outz.close();
}
