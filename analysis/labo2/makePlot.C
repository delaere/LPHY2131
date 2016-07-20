// this macro allows to make a standard plot with data and monte carlo superimposed
// it is useful once the cuts have been decided
{
// constants
TString var = "invMass";
Int_t bins = 90;
Float_t low = 40;
Float_t high = 150;
// change the scale factor given by Zyield here
Float_t scale_factor = 0.1;
// the changes in cuts must be done here
TString cuts = "nMuons==0 && nElectrons==2 && nJets==0";
// change "Ntuplefiles" with the name of Ntuples files of either electrons or muons
TFile* data_file = TFile::Open("Ntuplefiles");
TFile* simu_file = TFile::Open("delpheAnalysisZ.root");

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
TF1 *func = new TF1("myVoigt", myVoigt ,80, 100,4);
func->SetParameter(0,1500.0);   func->SetParName(0,"const");
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

