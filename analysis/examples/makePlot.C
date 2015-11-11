// this macro allows to make a standard plot with data and monte carlo superimposed
// it is useful once the cuts have been decided
{
// constants
TString var = "invMass";
Int_t bins = 100;
Float_t low = 0;
Float_t high = 100;
Float_t scale_factor = 0.1;
TString cuts = "nElectrons==2 && ElectronsPt[0]>20 && (Long64_t)33 electronIsolation[0]* electronIsolation[1]<0.001";
TFile* data_file = TFile::Open("data.root");
TFile* simu_file = TFile::Open("simu.root");

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
simu_file->cd();
hsimu->SetDirectory(gDirectory);
WeakBosonsAnalysis->Draw(Form("%s>>%s_simu",(const char*)var,(const char*)var),cuts,"HIST SAME");
hsimu->Scale(scale_factor);
hsimu->SetFillColor(kYellow);

// fit the data (only makes sense for the Z mass plot)
TF1 *func = new TF1("myVoigt", myVoigt ,low, high,4);
func->SetParameter(0,10.0);   func->SetParName(0,"const");
func->SetParameter(1,90.0);   func->SetParName(1,"mean");
func->SetParameter(2,3.0);    func->SetParName(2,"sigma");
func->SetParameter(3,3.0);    func->SetParName(3,"gamma");
hdata->Fit("myVoigt","LLR","SAME");
TF1 *fit = hsimu->GetFunction("myVoigt");
if(fit) fit->SetLineColor(kRed);

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

