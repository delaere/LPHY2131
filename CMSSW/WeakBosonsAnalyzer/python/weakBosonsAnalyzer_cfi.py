import FWCore.ParameterSet.Config as cms

weakBosonsAnalyzer = cms.EDAnalyzer('WeakBosonsAnalyzer'
                      ,patMuons = cms.untracked.InputTag('generalTracks')
                      ,patElectrons = cms.untracked.InputTag('generalTracks')
                      ,tracks = cms.untracked.InputTag('generalTracks')
                      ,patJets = cms.untracked.InputTag('generalTracks')
                      ,SkipEvent = cms.untracked.vstring('ProductNotFound')
                      ,patMET = cms.untracked.InputTag('generalTracks')
)
