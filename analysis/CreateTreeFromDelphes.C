// reads the Delphes output files and outputs an analysis TTree
// the output has the same format/content as the analysis TTree created in CMSSW, which allows to analyze data and Monte Carlo the same way.

#include <vector>
#include <algorithm>    // std::sort
#include <math.h> 
#include <iostream> 
#include "classes/DelphesClasses.h"
#include "TSystem.h"
#include "TRandom.h"
#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TClonesArray.h"
#include "external/ExRootAnalysis/ExRootTreeReader.h"

// usage: root -l CreateTreeFromDelphes.C(input.root, output.root)

//Function used to sort muons by Pt
bool sortMuonsByPt(Muon* mu1, Muon* mu2){return mu1->PT > mu2->PT;}

//Function used to sort electrons by Pt
bool sortElectronsByPt(Electron* el1, Electron* el2){return el1->PT > el2->PT;}

//Main function
void CreateTreeFromDelphes(TString input, TString output_tree)
{       
   // open the file
   TChain chain("Delphes");
   chain.Add(input);

   // open the file content, and select the relevant inputs
   ExRootTreeReader *treeReader = new ExRootTreeReader(&chain);
   TClonesArray *branchMuon = treeReader->UseBranch("Muon");
   TClonesArray *branchElectron = treeReader->UseBranch("Electron");
   TClonesArray *branchMissingET = treeReader->UseBranch("MissingET");
   TClonesArray *branchJet = treeReader->UseBranch("Jet");
   // get the number of entries (events)
   Long64_t nev = treeReader->GetEntries();

   // declare the variables used for the output TTree
   Double_t invMass, transvMass, dileptonPt, dileptonEta, dileptonPhi;
   Double_t MET_pt, MET_eta, MET_phi, dileptondeltaR, dileptondeltaPhi;
   Double_t MuonsPt[20], MuonsEta[20], MuonsPhi[20], ElectronsPt[20], ElectronsEta[20], ElectronsPhi[20], MuonIsolation[20], ElectronIsolation[20] ;
   Double_t JetsPt[20], JetsEta[20], JetsPhi[20];
   Int_t nMuons, nElectrons, nJets, Wcharge;
   unsigned int nmuons, nelectrons, njets;
   // create output
   TFile *file = new TFile(output_tree,"create");
   TDirectory * LPHY2131analysisDir = file->mkdir("LPHY2131analysis");
   LPHY2131analysisDir->cd();
   TTree *T = new TTree("WeakBosonsAnalysis","WeakBosonsAnalysis");
   // define the branches in the output
   T->Branch("nMuons",&nMuons,"nMuons/I");
   T->Branch("MuonsPt",MuonsPt,"MuonsPt[nMuons]/D");
   T->Branch("MuonsEta",MuonsEta,"MuonsEta[nMuons]/D");
   T->Branch("MuonsPhi",MuonsPhi,"MuonsPhi[nMuons]/D");
   T->Branch("nElectrons",&nElectrons,"nElectrons/I");
   T->Branch("ElectronsPt",ElectronsPt,"ElectronsPt[nElectrons]/D");
   T->Branch("ElectronsEta",ElectronsEta,"ElectronsEta[nElectrons]/D");
   T->Branch("ElectronsPhi",ElectronsPhi,"ElectronsPhi[nElectrons]/D");
   T->Branch("invMass",&invMass,"invMass/D");
   T->Branch("transvMass",&transvMass,"transvMass/D");
   T->Branch("dileptonPt",&dileptonPt,"dileptonPt/D");
   T->Branch("dileptonEta",&dileptonEta,"dileptonEta/D");
   T->Branch("dileptonPhi",&dileptonPhi,"dileptonPhi/D");
   T->Branch("dileptondeltaR",&dileptondeltaR,"dileptondeltaR/D");
   T->Branch("dileptondeltaPhi",&dileptondeltaPhi,"dileptondeltaPhi/D");
   T->Branch("MET_pt", &MET_pt, "MET_pt/D");
   T->Branch("MET_phi",&MET_phi,"MET_phi/D");
   T->Branch("MET_eta",&MET_eta,"MET_eta/D");
   T->Branch("nJets",&nJets,"nJets/I");
   T->Branch("JetsPt",JetsPt,"JetsPt[nJets]/D");
   T->Branch("JetsEta",JetsEta,"JetsEta[nJets]/D");
   T->Branch("JetsPhi",JetsPhi,"JetsPhi[nJets]/D");
   T->Branch("MuonIsolation",MuonIsolation,"MuonIsolation[nMuons]/D");
   T->Branch("ElectronIsolation",ElectronIsolation,"ElectronIsolation[nElectrons]/D");
   T->Branch("Wcharge",&Wcharge,"Wcharge/I");

   // loop over the events in the input
   for(Int_t entries = 0; entries < nev; ++entries) {

      Double_t deltaR;
      vector <Muon*> vecMuons;
      vector <Electron*> vecElectrons;
      vector <Jet*> vecJets;
      invMass=-1;
      transvMass=-1;

      // read the event
      treeReader->ReadEntry(entries);

      // count the objects
      njets = branchJet->GetEntries();
      nelectrons = branchElectron->GetEntries();
      nmuons = branchMuon->GetEntries();

      // loop over muons, and select those that are high-Pt and isolated
      for(unsigned int i =0; i<nmuons; ++i){
         Muon *poss_mu = (Muon *) branchMuon->At(i);     
         if((poss_mu->SumPtNeutral)/(poss_mu->PT)<=0.1){
            vecMuons.push_back(poss_mu);
         }
      }
      nMuons=vecMuons.size(); 
      // sort the collection by Pt
      std::sort(vecMuons.begin(),vecMuons.end(),sortMuonsByPt);
      // fill branches
      for(unsigned int i = 0; i<vecMuons.size(); ++i) {
        MuonsPt[i] = vecMuons[i]->PT;
        MuonsEta[i] = vecMuons[i]->Eta;
        MuonsPhi[i] = vecMuons[i]->Phi;
        MuonIsolation[i] = vecMuons[i]->SumPtNeutral/vecMuons[i]->PT;       
      }

      // loop over electrons, and select those that are high-Pt and isolated
      for(unsigned int i =0; i<nelectrons; ++i){
         Electron *poss_ele = (Electron *) branchElectron->At(i);
         if((poss_ele->SumPtNeutral)/(poss_ele->PT)<=0.1){
            vecElectrons.push_back(poss_ele);
         }
      }
      nElectrons=vecElectrons.size(); 
      // sort the collection by Pt
      std::sort(vecElectrons.begin(),vecElectrons.end(),sortElectronsByPt);
      // fill the branches
      for(unsigned int i = 0; i<vecElectrons.size(); ++i) {
         ElectronsPt[i] = vecElectrons[i]->PT;
         ElectronsEta[i] = vecElectrons[i]->Eta;
         ElectronsPhi[i] = vecElectrons[i]->Phi;
         ElectronIsolation[i] = vecElectrons[i]->SumPtNeutral/vecElectrons[i]->PT; 
      }

      int z=0;
      int a=1;
      int b=1;
      // loop over the jets
      for(unsigned int i=0; i<njets; ++i){
         a=1;
         b=1;
         Jet *jet =  (Jet*) branchJet->At(i);
         // make sure that the jet is far from any muon
         for(unsigned int j=0; j<vecMuons.size(); ++j){
            Muon *muon = vecMuons[j];
            deltaR = sqrt( pow( ((muon->Phi)-(jet->Phi)),2 )+pow( ((muon->Eta)-(jet->Eta)),2 ) );
            if (deltaR<0.1){a=0;break;}
         }
         if(a==0) continue;
         // make sure that the jet is far from any electron
         for(unsigned int k=0; k<vecElectrons.size(); ++k){
            Electron *elec = vecElectrons[k];
            deltaR = sqrt( pow( ((elec->Phi)-(jet->Phi)),2 )+pow( ((elec->Eta)-(jet->Eta)),2 ) );
            if (deltaR<0.1){b=0;break;}
         }
         if(b==0) continue;
         // if all the conditions are passed, store pt, eta, phi
         vecJets.push_back(jet);
         JetsEta[z]=jet->Eta;
         JetsPhi[z]=jet->Phi;
         JetsPt[z]=jet->PT;
         ++z;
      }
      // count the selected jets
      nJets = vecJets.size();
   
      // missing transverse energy
      MissingET *met = (MissingET*)branchMissingET->At(0);
      MET_pt = met->MET + gRandom->Gaus(0,6); // artificial smearing to fit data
      MET_phi= met->Phi;
      MET_eta= met->Eta;

      // compute the invariant mass of the leading leptons
      TLorentzVector dilepton(0.,0.,0.,0.);
      if(nMuons>=2) {
         dileptondeltaR = vecMuons[0]->P4().DeltaR(vecMuons[1]->P4());
         dileptondeltaPhi = vecMuons[0]->P4().DeltaPhi(vecMuons[1]->P4());
         dilepton = vecMuons[0]->P4()+vecMuons[1]->P4();
      } else if(nElectrons>=2) {
         dileptondeltaR = vecElectrons[0]->P4().DeltaR(vecElectrons[1]->P4());
         dileptondeltaPhi = vecElectrons[0]->P4().DeltaPhi(vecElectrons[1]->P4());
         dilepton = vecElectrons[0]->P4() + vecElectrons[1]->P4();
      } else if(nElectrons==1 && nMuons==1) {
         dileptondeltaR = vecElectrons[0]->P4().DeltaR(vecMuons[0]->P4());
         dileptondeltaPhi = vecElectrons[0]->P4().DeltaPhi(vecMuons[0]->P4());
         dilepton = vecElectrons[0]->P4() + vecMuons[0]->P4();
      }
      invMass     = dilepton.M();
      dileptonPt  = dilepton.Pt();
      dileptonEta = dilepton.Eta();
      dileptonPhi = dilepton.Phi();

      // compute the transverse mass using the leading lepton and MET
      Wcharge = 0;
      if(nMuons>=1){
         double dphi = vecMuons[0]->P4().DeltaPhi(met->P4());
         transvMass = sqrt(2*MuonsPt[0]*MET_pt*(1-cos(dphi)));
         Wcharge = vecMuons[0]->Charge;
      }
      else if(nElectrons>=1){
         double dphi = vecElectrons[0]->P4().DeltaPhi(met->P4());
         transvMass = sqrt(2*ElectronsPt[0]*MET_pt*(1-cos(dphi)));
         Wcharge = vecElectrons[0]->Charge;
      }

      // finally fill the output tree for that event
      T->Fill();
   }
   
   // write the output file     
   file->Write();
   file->Close();
   delete file;
}
