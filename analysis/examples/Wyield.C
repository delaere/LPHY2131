// this macro allows to make a standard plot with data and monte carlo superimposed
// while fitting the signal and background to data
// signal comes from MC
// background from a control data sample
{
// constants
TString var = "transvMass";
Int_t bins = 20;
Float_t low = 40;
Float_t high = 100;
TString cuts_signalregion  = "nElectrons>=1";
TString cuts_controlregion = "nElectrons>=1";
TFile* data_file = TFile::Open("LPHY2131tree.root");
TFile* simu_file = TFile::Open("delpheAnalysisW.root");
Float_t scale_factor = 1.;

// some initialization
gROOT->LoadMacro("functions.C");
gStyle->SetOptFit(111111);

// create the histograms to fill
TH1F* hdata = new TH1F(Form("%s_data",(const char*)var),var,bins,low,high);
hdata->Sumw2();
TH1F* hsimu = new TH1F(Form("%s_simu",(const char*)var),var,bins,low,high);
hsimu->Sumw2();
TH1F* hbkg = new TH1F(Form("%s_bkg",(const char*)var),var,bins,low,high);
hbkg->Sumw2();

// fill and draw the histograms
new TCanvas;
data_file->cd("LPHY2131analysis");
hdata->SetDirectory(gDirectory);
WeakBosonsAnalysis->Draw(Form("%s>>%s_data",(const char*)var,(const char*)var),cuts_signalregion,"E0 P0");
hdata->SetMarkerStyle(20);
hbkg->SetDirectory(gDirectory);
WeakBosonsAnalysis->Draw(Form("%s>>%s_bkg",(const char*)var,(const char*)var),cuts_controlregion,"HIST SAME");
hbkg->SetFillColor(kBlue);
simu_file->cd();
hsimu->SetDirectory(gDirectory);
WeakBosonsAnalysis->Draw(Form("%s>>%s_simu",(const char*)var,(const char*)var),cuts_signalregion,"HIST SAME");
hsimu->Scale(scale_factor);
hsimu->SetFillColor(kYellow);
hdata->Draw("same");

// do the fit
new TCanvas;
TObjArray *contributions = new TObjArray(2);
contributions->Add(hbkg);
contributions->Add(hsimu);
TFractionFitter* fit = new TFractionFitter(hdata,contributions);
fit->Constrain(0,0.0,1.0);
fit->Constrain(1,0.0,1.0);
fit->Fit();
hdata->Draw();
fit->GetPlot()->Draw("same");

// combined plot
new TCanvas;
Double_t value,error;
fit->GetResult(0,value,error);
float bkg_sf = hdata->Integral()*value/hbkg->Integral();
fit->GetResult(1,value,error);
float sig_sf = hdata->Integral()*value/hsimu->Integral();
hbkg->Scale(bkg_sf);
hsimu->Scale(sig_sf);
THStack* stack = new THStack;
stack->Add(hbkg);
stack->Add(hsimu);
stack->Draw("hist");
hdata->Draw("same");

// add a legend
leg = new TLegend(0.15, 0.68, 0.35,0.88);
leg->AddEntry(hdata,"data","l");
leg->AddEntry(hsimu,"signal MC (NLO)","f");
leg->AddEntry(hbkg,"background (from data)","f");
leg->SetBorderSize(0);
leg->SetShadowColor(0);
leg->SetFillColor(0);
leg->Draw("same");

// some final printout

std::cout << "estimated number of signal events: " << hdata->Integral()*value << std::endl;
std::cout << "corresponding scale factor: " << hdata->Integral()*value/hsimu->GetEntries() << std::endl;

// conclude
gPad->Update();
}

