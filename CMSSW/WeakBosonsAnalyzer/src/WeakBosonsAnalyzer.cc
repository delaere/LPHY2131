#include <memory>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include "TTree.h"
#include "Math/VectorUtil.h"

//
// class declaration
//
class WeakBosonsAnalyzer : public edm::EDAnalyzer {
   public:
      explicit WeakBosonsAnalyzer(const edm::ParameterSet&);
      ~WeakBosonsAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

// ----------member data ---------------------------
  edm::InputTag muonTags_;
  edm::InputTag electronTags_;
  edm::InputTag jetTags_;
  edm::InputTag metTags_;

  TTree *t_wzDecay;

  float invMass, transvMass, dileptonPt, dileptonEta, dileptonPhi;
  float MET_pt, MET_phi, MET_eta, dileptondeltaR, dileptondeltaPhi;
  float MuonsPt[20], MuonsEta[20], MuonsPhi[20], MuonIsolation[20];
  float ElectronsPt[20],ElectronsEta[20], ElectronsPhi[20], ElectronIsolation[20];
  float JetsPt[20], JetsEta[20], JetsPhi[20];
  int nMuons, nElectrons, nJets, Wcharge;
  Double_t deltaR;
};

//
// constants, enums and typedefs
//
  const double highPtThreshold = 10;
  const double highPtThresholdJets = 20;
  const double pi = 3.14159265358979;
//
// static data member definitions
//

//Function used to sort muons by Pt
bool sortMuonsByPt(pat::Muon mu1, pat::Muon mu2){return mu1.pt() > mu2.pt();}
 
//Function used to sort electrons by Pt
bool sortElectronsByPt(pat::Electron el1, pat::Electron el2){return el1.pt() > el2.pt();}

//
// constructors and destructor
//
WeakBosonsAnalyzer::WeakBosonsAnalyzer(const edm::ParameterSet& iConfig):
  muonTags_(iConfig.getUntrackedParameter<edm::InputTag>("patMuons")),
  electronTags_(iConfig.getUntrackedParameter<edm::InputTag>("patElectrons")),
  jetTags_(iConfig.getUntrackedParameter<edm::InputTag>("patJets")),
  metTags_(iConfig.getUntrackedParameter<edm::InputTag>("patMET"))
{  
}

WeakBosonsAnalyzer::~WeakBosonsAnalyzer()
{
}

//
// function called for every event
//
void WeakBosonsAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {  
   using namespace edm;
      
   // initialize the counters
   nElectrons = 0;
   nMuons = 0;
   nJets = 0;

   // access the MET collection (size 1) and fill retrieve Pt, eta, phi
   // the way this is coded, the values of the last entry are used. Since the size is always 1, this is fine.
   using pat::METCollection;
   Handle<pat::METCollection> patMET;
   iEvent.getByLabel(metTags_,patMET);
   for(pat::METCollection::const_iterator itMET = patMET->begin(); itMET != patMET->end(); ++itMET) {
     MET_pt = itMET->pt();
     MET_phi = itMET->phi();
     MET_eta = itMET->eta();
   }

   // access the muon collection
   using pat::MuonCollection;
   Handle<pat::MuonCollection> patMuons;
   iEvent.getByLabel(muonTags_,patMuons);
   pat::MuonCollection selectedMuons;  

   // filter the muons based on pt and relative isolation
   for(pat::MuonCollection::const_iterator itMuon = patMuons->begin(); itMuon != patMuons->end(); ++itMuon) {
     if(itMuon->pt() > highPtThreshold && itMuon->caloIso()/itMuon->pt() < 1){
       selectedMuons.push_back(*itMuon);
     }
   }
   // count the selected muons
   nMuons = selectedMuons.size();
   nMuons = nMuons<20 ? nMuons : 20;
   // sort the collection by Pt
   std::sort(selectedMuons.begin(),selectedMuons.end(),sortMuonsByPt);
   // loop on the selected muons and extract Pt, eta, phi, isolation
   unsigned int muoncnt = 0;
   for(pat::MuonCollection::const_iterator itMuon = selectedMuons.begin(); itMuon != selectedMuons.end(); ++itMuon, ++muoncnt) {
     if(muoncnt==20) {
       std::cerr << "Max number of muons reached" << std::endl;
       break;
     }
     MuonsPt[muoncnt]  = itMuon->pt();
     MuonsEta[muoncnt] = itMuon->eta();
     MuonsPhi[muoncnt] = itMuon->phi();
     MuonIsolation[muoncnt] = itMuon->caloIso() / itMuon->pt();
   }

   // access the electron collection
   using pat::ElectronCollection;
   Handle<pat::ElectronCollection> patElectrons;
   iEvent.getByLabel(electronTags_,patElectrons);
   pat::ElectronCollection selectedElectrons;  

   // filter the electrons based on pt and relative isolation
   for(pat::ElectronCollection::const_iterator itElectron = patElectrons->begin(); itElectron != patElectrons->end(); ++itElectron) {
     if(itElectron->pt() > highPtThreshold && itElectron->caloIso()/itElectron->pt() < 1){
       selectedElectrons.push_back(*itElectron);
     }
   }
   // count the selected electrons
   nElectrons = selectedElectrons.size();
   nElectrons = nElectrons<20 ? nElectrons : 20;
   // sort the collection by Pt
   std::sort(selectedElectrons.begin(),selectedElectrons.end(),sortElectronsByPt);
   // loop on the selected muons and extract Pt, eta, phi, isolation
   unsigned int electroncnt = 0;
   for(pat::ElectronCollection::const_iterator itElectron = selectedElectrons.begin(); itElectron != selectedElectrons.end(); ++itElectron, ++electroncnt) {
     if(electroncnt==20) {
       std::cerr << "Max number of electrons reached" << std::endl;
       break;
     }
     ElectronsPt[electroncnt] = itElectron->pt();
     ElectronsEta[electroncnt] = itElectron->eta();
     ElectronsPhi[electroncnt] = itElectron->phi();
     ElectronIsolation[electroncnt] = itElectron->caloIso() / itElectron->pt();
   }
   
   // access the jet collection
   using pat::JetCollection;
   Handle<pat::JetCollection> patJets;
   iEvent.getByLabel(jetTags_,patJets);
   pat::JetCollection selectedJets;

   // loop on the jet collection and filter them
   int z=0;
   int a=1;
   int b=1;
   for(pat::JetCollection::const_iterator itJet = patJets->begin(); itJet != patJets->end(); ++itJet) {
      a=1;
      b=1;
      // pt cut
      if(itJet->pt() < highPtThresholdJets){
        continue;
      }
      // make sure that the jet is "far" from any muon
      for(int j=0; j<nMuons; ++j){
         deltaR = sqrt( pow( ((selectedMuons[j].phi())-(itJet->phi())),2 )+pow( ((selectedMuons[j].eta())-(itJet->eta())),2 ) );
         if (deltaR<0.1){a=0; break;}
      }
      if(a==0) continue;
      // make sure that the jet is "far" from any electron
      for(int j=0; j<nElectrons; ++j){
         deltaR = sqrt( pow( ((selectedElectrons[j].phi())-(itJet->phi())),2 )+pow( ((selectedElectrons[j].eta())-(itJet->eta())),2 ) );
         if (deltaR<0.1){b=0; break;}
      }
      if(b==0) continue;
      // if all the conditions are passed, store pt, eta, phi
      selectedJets.push_back(*itJet);
      JetsPt[z] = itJet->pt();
      JetsEta[z] = itJet->eta();
      JetsPhi[z] = itJet->phi();
      ++z;
   }
   // count the selected jets
   nJets = selectedJets.size();

   // initialize some values to -1. This is the default if no dilepton pair is present.
   invMass = -1.;
   transvMass = -1.;
   dileptondeltaR = -1.;
   dileptondeltaPhi= -1.;

   // if there is at least one lepton, compute the transverse mass
   Wcharge = 0;
   if(selectedMuons.size() > 0) {
     double dphi = fabs(fabs(fabs(MuonsPhi[0]-MET_phi)-TMath::Pi())-TMath::Pi());
     transvMass = sqrt(2*MuonsPt[0]*MET_pt*(1-cos(dphi)));
     Wcharge = selectedMuons[0].charge();
   } else if (selectedElectrons.size() > 0){
     double dphi = fabs(fabs(fabs(ElectronsPhi[0]-MET_phi)-TMath::Pi())-TMath::Pi());
     transvMass = sqrt(2*ElectronsPt[0]*MET_pt*(1-cos(dphi)));
     Wcharge = selectedElectrons[0].charge();
   }

   // if an electron pair is found, combine into a Z candidate
   // Here, we take the two leading-Pt leptons. We could be clever but the difference is small.
   reco::Candidate::LorentzVector p4CM;
   if (selectedElectrons.size() >= 2){
      p4CM = selectedElectrons[0].p4() + selectedElectrons[1].p4();
      dileptondeltaR   = ROOT::Math::VectorUtil::DeltaR(selectedElectrons[0].p4(),selectedElectrons[1].p4());
      dileptondeltaPhi = ROOT::Math::VectorUtil::DeltaPhi(selectedElectrons[0].p4(),selectedElectrons[1].p4());
   // otherwise, if a muon pair is found, combine into a Z candidate.
   // Again, we take the two leading-Pt leptons. We could be clever but the difference is small.
   } else if(selectedMuons.size() >= 2) {
      p4CM = selectedMuons[0].p4() + selectedMuons[1].p4();
      dileptondeltaR   = ROOT::Math::VectorUtil::DeltaR(selectedMuons[0].p4(),selectedMuons[1].p4());
      dileptondeltaPhi = ROOT::Math::VectorUtil::DeltaPhi(selectedMuons[0].p4(),selectedMuons[1].p4());
   // last case: one electron and one muons.
   } else if (selectedMuons.size() == 1 && selectedElectrons.size() == 1) {
      p4CM = selectedMuons[0].p4() + selectedElectrons[0].p4();
      dileptondeltaR   = ROOT::Math::VectorUtil::DeltaR(selectedMuons[0].p4(),selectedElectrons[0].p4());
      dileptondeltaPhi = ROOT::Math::VectorUtil::DeltaPhi(selectedMuons[0].p4(),selectedElectrons[0].p4());
   }
   invMass     = p4CM.mass();
   dileptonPt  = p4CM.pt();
   dileptonEta = p4CM.eta();
   dileptonPhi = p4CM.phi();
   // write all to the result TTree
   t_wzDecay->Fill();
}

// ------------ method called once each job just before starting event loop  ------------
void 
WeakBosonsAnalyzer::beginJob()
{
   //now do what ever initialization is needed
  edm::Service<TFileService> fs;
 
  t_wzDecay = fs->make<TTree>("WeakBosonsAnalysis","WeakBosonsAnalysis");

  t_wzDecay->Branch("nMuons",&nMuons,"nMuons/I");   
  t_wzDecay->Branch("MuonsPt",MuonsPt,"MuonsPt[nMuons]/F"); 
  t_wzDecay->Branch("MuonsEta",MuonsEta,"MuonsEta[nMuons]/F");
  t_wzDecay->Branch("MuonsPhi",MuonsPhi,"MuonsPhi[nMuons]/F");
  t_wzDecay->Branch("nElectrons",&nElectrons,"nElectrons/I"); 
  t_wzDecay->Branch("ElectronsPt",ElectronsPt,"ElectronsPt[nElectrons]/F");
  t_wzDecay->Branch("ElectronsEta",ElectronsEta,"ElectronsEta[nElectrons]/F");
  t_wzDecay->Branch("ElectronsPhi",ElectronsPhi,"ElectronsPhi[nElectrons]/F");
  t_wzDecay->Branch("invMass",&invMass,"invMass/F");
  t_wzDecay->Branch("transvMass",&transvMass,"transvMass/F");
  t_wzDecay->Branch("dileptonPt",&dileptonPt,"dileptonPt/F");
  t_wzDecay->Branch("dileptonEta",&dileptonEta,"dileptonEta/F");
  t_wzDecay->Branch("dileptonPhi",&dileptonPhi,"dileptonPhi/F");
  t_wzDecay->Branch("dileptondeltaR",&dileptondeltaR,"dileptondeltaR/F");
  t_wzDecay->Branch("dileptondeltaPhi",&dileptondeltaPhi,"dileptondeltaPhi/F");
  t_wzDecay->Branch("MET_pt",&MET_pt,"MET_pt/F");
  t_wzDecay->Branch("MET_phi",&MET_phi,"MET_phi/F");
  t_wzDecay->Branch("MET_eta",&MET_eta,"MET_eta/F");
  t_wzDecay->Branch("nJets",&nJets,"nJets/I");
  t_wzDecay->Branch("JetsPt",JetsPt,"JetsPt[nJets]/F"); 
  t_wzDecay->Branch("JetsEta",JetsEta,"JetsEta[nJets]/F");
  t_wzDecay->Branch("JetsPhi",JetsPhi,"JetsPhi[nJets]/F");
  t_wzDecay->Branch("MuonIsolation",MuonIsolation,"muonIsolation[nMuons]/F");
  t_wzDecay->Branch("ElectronIsolation",ElectronIsolation,"electronIsolation[nElectrons]/F");
  t_wzDecay->Branch("Wcharge",&Wcharge,"Wcharge/I");
}

// ------------ method called once each job just after ending the event loop  ------------
void 
WeakBosonsAnalyzer::endJob() 
{
  edm::Service<TFileService> fs;
}

// ------------ method called when starting to processes a run  ------------
void 
WeakBosonsAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
WeakBosonsAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
WeakBosonsAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
WeakBosonsAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
WeakBosonsAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

 //Specify that only 'tracks' is allowed
 //To use, remove the default given above and uncomment below
 //ParameterSetDescription desc;
 //desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
 //descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(WeakBosonsAnalyzer);
