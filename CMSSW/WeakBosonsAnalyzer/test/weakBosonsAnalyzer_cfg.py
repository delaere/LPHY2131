import FWCore.ParameterSet.Config as cms

process = cms.Process("ZDecay")
process.load("FWCore.MessageService.MessageLogger_cfi")
#show the message of run every 1000 events to improve the speed of the analyze
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# maximum number of events to be processed
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# if ever information is missing for an event, skip instead of crashing
process.options = cms.untracked.PSet( SkipEvent = cms.untracked.vstring('ProductNotFound')
)

# input files
# for local files, use "file://" followed by the absolute path
# for files at CERN on eos, use "root://eospublic.cern.ch/" followed by the eos path.
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #PAT fils contazining the data for double muons
        "file:///home/cms-opendata/LPHY2131_data/doubleMu2011_PAT.root"     
    )
)

# analysis
# parameters are the input tags for each collection
process.LPHY2131analysis = cms.EDAnalyzer('WeakBosonsAnalyzer'
                                  , tracks = cms.untracked.InputTag('tracks')
                                  , patMuons = cms.untracked.InputTag('cleanPatMuons')
                                  , patElectrons = cms.untracked.InputTag('cleanPatElectrons')
                                  , patJets = cms.untracked.InputTag('cleanPatJets')
                                  , patMET = cms.untracked.InputTag('patMETs')
                           )

# output
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('LPHY2131tree.root')
                                  )

# sequence to run: just the analysis.
process.p = cms.Path(process.LPHY2131analysis)
