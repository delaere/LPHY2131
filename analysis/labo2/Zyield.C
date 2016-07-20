// this macro measures the signal yield
// it is useful once the cuts have been decided in order to determine the scale factor for MC (and therefore the luminosity or the cross-section)

{
// constants to be adapted
TString var = "invMass";
Int_t bins = 30;
Float_t low = 50;
Float_t high = 140;
// the changes in cuts must be done here
TString cuts = "nElectrons==2";
// files
// change "Ntuplefiles" with the name of Ntuples files of either electrons or muons
TFile* data_file = TFile::Open("Ntuplefiles");
TFile* simu_file = TFile::Open("delpheAnalysisZ.root");
// analytical form for the background
TF1* f0 = new TF1("bkg","[0]+[1]*x",50,140); //to be adapted
f0->SetParameter(1,-0.02); //to be adapted
f0->SetParameter(0,3.); //to be adapted

// some initialization
gROOT->LoadMacro("functions.C");
gStyle->SetOptFit(111111);

// create the histograms to fill
TH1F* hdata = new TH1F(Form("%s_data",(const char*)var),var,bins,low,high);
hdata->Sumw2();
TH1F* hsimu = new TH1F(Form("%s_simu",(const char*)var),var,bins,low,high);
hsimu->Sumw2();
TH1F* hbackground = new TH1F(Form("%s_bkg",(const char*)var),var,bins,low,high);
hbackground->Sumw2();
hbackground->SetDirectory(0);

// fill and draw the histograms
// hdata is the data histogram
// hsimu is the MC signal (Drell-Yann)
// hbackground is the background shape. The analytical form can be changed.
new TCanvas;
data_file->cd("LPHY2131analysis");
hdata->SetDirectory(gDirectory);
WeakBosonsAnalysis->Draw(Form("%s>>%s_data",(const char*)var,(const char*)var),cuts,"E0 P0");
hdata->SetMarkerStyle(20);
simu_file->cd();
hsimu->SetDirectory(gDirectory);
WeakBosonsAnalysis->Draw(Form("%s>>%s_simu",(const char*)var,(const char*)var),cuts,"HIST SAME");
hsimu->SetFillColor(kYellow);
for( Int_t i=0; i<10000; i++) {
  hbackground->Fill( f0->GetRandom() );
}

// do the fit
TObjArray *mc = new TObjArray(2);
mc->Add(hsimu);
mc->Add(hbackground);
TFractionFitter* fit = new TFractionFitter(hdata, mc);
fit->Constrain(0,0.0,1.0);
fit->Constrain(1,0.0,1.0);
fit->Fit();

// get the result
hdata->Draw(); // draw data
fit->GetPlot()->Draw("same"); // draw fit outcome: signal+background
Double_t value,error;
fit->GetResult(0,value,error);
std::cout << "Purity: " << value << " +/- " << error << std::endl;
std::cout << "Scale Factor: " << hdata->Integral()*value/hsimu->Integral() << std::endl;
std::cout << "N_mc = " << hsimu->Integral() << std::endl;
std::cout << "N_data = " << hdata->Integral() << std::endl;
std::cout << "N_Z = " << hdata->Integral()*value << std::endl;
std::cout << "N_bkg = " << hdata->Integral()*(1-value) << std::endl;
hsimu->Scale(hdata->Integral()*value/hsimu->Integral());
hsimu->Draw("same histo"); // draw the scaled signal alone
hdata->Draw("same"); // redraw data on top

// conclude
gPad->Update();

}

