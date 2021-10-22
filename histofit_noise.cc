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
for (int i=0; i<period; i++){
	file[i]->cd();
       	histz[i] = (TH1F*) QwZPosBeam_tOff->Clone();
}



// Plot formatting
histz[0]->SetLineWidth(2);
histz[0]->SetLineColor(1);
//histx[0]->GetYaxis()->SetRangeUser(0.,0.8);
for (int i=1; i<period; i++){
	histz[i]->SetLineWidth(2);
	histz[i]->SetLineColor(2);
}

ofstream outz;
char foutz[200];
sprintf(foutz,"data/B%d_noise.txt",injpos);
outz.open(foutz);
outz << "Year  Month  Day  Const.  C_error " << endl;
outz << "----------------------------------" << endl;

for (int i=0; i<period; i++){
	histz[i]->Draw("hist");
	histz[i]->Fit("pol0","Q");
	pol0->Draw("same");
	outz << dt[i]->GetYear() << "-" << dt[i]->GetMonth() << "-" << dt[i]->GetDay() << " " << pol0->GetParameter(0) << " " << pol0->GetParError(0) << endl;
//	legz[i]->Draw();
	c1->Update();
//  	if (i==0) c1->SaveAs("gplots_noise.pdf(");
//	else if (i==period-1) c1->SaveAs("gplots_noise.pdf)");
//	else c1->SaveAs("gplots_noise.pdf");
}

outz.close();
}
