// this macro allows to make a standard plot with data and monte carlo superimposed
// it is useful once the cuts have been decided
{

///////////////////////////////////////////////////////////////////////////////
//  CONFIGURATION                                                            //
///////////////////////////////////////////////////////////////////////////////

// constants to be adapted if you want
TString var = "invMass";
Int_t bins = 90;
Float_t low = 40;
Float_t high = 150;
// change the scale factor given by Zyield here
Float_t scale_factor = 297.951;
// the changes in cuts must be done here
TString cuts = "nElectrons==2";
// input files
// these points to the default files for this lab. 
// data_file is the data ntuple you want to use. Pick either electrons or muons 
// by uncommenting one of the lines below.
//TFile* data_file = TFile::Open("doubleEl2011_ntuple.root");
//TFile* data_file = TFile::Open("doubleMu2011_ntuple.root");
TFile* simu_file = TFile::Open("delpheAnalysisZ.root");

///////////////////////////////////////////////////////////////////////////////
//  ANALYSIS SCRIPT - MAKE A STANDARD PLOT WITH DATA AND MONTE CARLO         //
///////////////////////////////////////////////////////////////////////////////

// some initialization
gROOT->LoadMacro("functions.C");
gStyle->SetOptFit(111111);

// create the histograms to fill
TH1F* hdata = new TH1F(Form("%s_data",(const char*)var),var,bins,low,high);
hdata->Sumw2();
TH1F* hsimu = new TH1F(Form("%s_simu",(const char*)var),var,bins,low,high);
hsimu->Sumw2();

// fill and draw the histograms
new TCanvas;
data_file->cd("LPHY2131analysis");
hdata->SetDirectory(gDirectory);
WeakBosonsAnalysis->Draw(Form("%s>>%s_data",(const char*)var,(const char*)var),cuts,"E0 P0");
hdata->SetMarkerStyle(20);
simu_file->cd("LPHY2131analysis");
hsimu->SetDirectory(gDirectory);
WeakBosonsAnalysis->Draw(Form("%s>>%s_simu",(const char*)var,(const char*)var),cuts,"HIST SAME");
hsimu->Scale(scale_factor);
hsimu->SetFillColor(kYellow);

// fit function (the fit only makes sense for the Z mass plot)
TF1 *func = new TF1("myVoigt", myVoigt ,40, 150,6);
func->SetParameter(0,1e5.0);   func->SetParName(0,"const");
func->SetParameter(1,90.0);    func->SetParName(1,"mean");
func->SetParameter(2,1.0);     func->SetParName(2,"sigma");
func->SetParameter(3,3.0);     func->SetParName(3,"gamma");
func->SetParameter(4,0);       func->SetParName(4,"BkgConst");
func->SetParameter(5,0);       func->SetParName(5,"BkgSlope");
func->SetParLimits(0,10,1e10);
func->SetParLimits(1,85,95);
func->SetParLimits(2,0,10);
func->SetParLimits(3,0,10);
func->SetParLimits(4,0,1000);
func->SetParLimits(5,-1,0);

// fit the MC with fixed BW width
func->FixParameter(3,2.4952);
hsimu->Fit("myVoigt","LLR","0");
TF1 *mcfit = hsimu->GetFunction("myVoigt");
func->SetParLimits(3,0,10);
//uncomment the line below to fix the resolution to the 
//one in simulation.
//func->FixParameter(2,mcfit->GetParameter(2));
delete mcfit;
hdata->Draw();
hsimu->Draw("HIST SAME");

// fit the data
TFitResultPtr r = hdata->Fit("myVoigt","LLRS","SAME");
TF1 *fit = hdata->GetFunction("myVoigt");
if(fit) {
   fit->SetLineColor(kRed);
   fit->SetNpx(1000);
}
r->Print("V");

// add a legend
leg = new TLegend(0.15, 0.68, 0.35,0.88);
leg->AddEntry(hdata,"data","l");
leg->AddEntry(hsimu,"MC (NLO)","f");
leg->SetBorderSize(0);
leg->SetShadowColor(0);
leg->SetFillColor(0);
leg->Draw("same");

// conclude
gPad->Update();
}

