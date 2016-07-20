import FWCore.ParameterSet.Config as cms

process = cms.Process("ZDecay")
process.load("FWCore.MessageService.MessageLogger_cfi")

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
        #Pat files containing the data for single electrons
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/0041C34D-0D3E-E311-95CE-02163E00BFFD.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/008F2296-0D3E-E311-8D7B-003048CF6CFA.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/00C5DD46-FD3D-E311-B71B-02163E00A40B.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/02565512-1D3E-E311-B2EE-0025901AF58A.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/02CBD831-F63D-E311-A4A2-003048CF98BE.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/02D74A3B-CE3D-E311-8E84-002590494D9C.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/04F98A5C-DF3D-E311-9B87-0025901D623E.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/061319CD-CE3D-E311-9490-5404A63886B0.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/064AECD5-F73D-E311-A1FC-003048F16F44.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/06922E84-D83D-E311-AC92-02163E00A0F7.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/06B8CFD2-EA3D-E311-AB9A-003048FEAFA0.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/08219E74-DD3D-E311-A01B-0025904B1F90.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/083E0BC9-1C3E-E311-A8E2-02163E00BA30.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/0881DA3E-033E-E311-B7A1-002590494FE2.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/20001/08E73487-D23D-E311-AF4A-003048F027EC.root'

        #Pat files containing the data for single muons
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/000683AB-1837-E311-A222-5404A6388698.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/000A46EA-2637-E311-BCE5-02163E008F08.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/001E486D-0B37-E311-A1DC-0030489452A2.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/0023BB65-FF36-E311-9EA4-003048FEB8EE.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/003249A0-A536-E311-B733-003048F1BF38.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/0033D712-2137-E311-B11B-003048CBAED4.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/004A575B-5537-E311-8DEA-0025904B11AE.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/00887384-3B37-E311-9248-003048F179BE.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/008887D4-2237-E311-BC31-02163E00AF67.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/00A23C6F-BE36-E311-BBFE-BCAEC5329701.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/00AC93BB-1037-E311-98C7-02163E00C4B4.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/00C8E8C3-F636-E311-B9AB-02163E008EF1.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/00F9AB11-4637-E311-B8EB-003048CF9E2C.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/022678D6-4937-E311-901B-003048F0E31C.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/02304642-0637-E311-8549-003048FEB93E.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/0244A56F-0B37-E311-93CE-0025904952A4.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/02578F96-F136-E311-AF86-003048CFAD08.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/0259F84A-A036-E311-9C46-003048FEB906.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/029A6195-E236-E311-82E4-002590494F78.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/02A734A0-1037-E311-A3EF-0025904B2C7A.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/02D75D48-0037-E311-87F4-003048CFAD0E.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/AOD/12Oct2013-v1/20000/02EED73E-4137-E311-85A5-003048F11CF0.root'
        
        #Pat files containing the data for double electrons
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/0014CE62-9C3E-E311-8FCC-00261894389F.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/003EF6D5-B83E-E311-8157-003048D42D92.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/0075E204-583E-E311-9749-00261894398C.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/0089898B-A23E-E311-83FD-0026189438F8.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/00CA715D-753E-E311-9B3B-00304867920A.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/00E14E66-8C3E-E311-8442-002618943810.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/02189AC0-6C3E-E311-9A67-002618943842.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/0224FE84-BF3E-E311-8592-002618943854.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/02843B55-613E-E311-B51E-00261894393C.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/028A7936-9B3E-E311-AEF5-002618943885.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/02C39E17-9D3E-E311-B5EF-003048FF86CA.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/02F78600-B13E-E311-9844-003048FF86CA.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/02FCC382-6F3E-E311-98B6-003048678F9C.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/043774CF-673E-E311-8805-0025905964B6.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/043CDE04-643E-E311-AC35-003048678FF8.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/AOD/12Oct2013-v1/20000/047E8887-813E-E311-AD8F-003048FFD756.root'
        
        #Pat fils contazining the data for double muons
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/045CCED6-033F-E311-9E93-003048678F74.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/0830BC83-043F-E311-A865-003048FFD752.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/0867387C-033F-E311-AFE0-0026189438A2.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/08C0954A-013F-E311-82AD-003048FFD720.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/10FF8BDD-033F-E311-99CB-002618FDA210.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/1A6B127D-033F-E311-988C-00261894380A.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/209BA10C-043F-E311-A8AA-002618943870.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/22317CE5-033F-E311-813C-00259059649C.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/2258E319-053F-E311-8C7F-003048678FF4.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/282677C4-013F-E311-B326-003048FFCBFC.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/2AD5A2C4-013F-E311-81DE-003048678B8E.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/2C52C47C-033F-E311-9F5B-002618943930.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/2C824348-013F-E311-BE95-002618FDA259.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/3EE43E7C-033F-E311-8B11-003048678F8C.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/44FC16D6-033F-E311-8DE3-002618FDA26D.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/4AD3031A-053F-E311-AF46-00261894380A.root'
        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleMu/AOD/12Oct2013-v1/20000/5631D17E-043F-E311-85F2-00304867903E.root'
        
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
