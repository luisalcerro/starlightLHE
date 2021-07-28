from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

# We want to put all the CRAB project directories from the tasks we submit here into one common directory.
# That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
from CRABClient.UserUtilities import config
config = config()

config.section_("General")
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step1_STARlight_LHE_GenSim_cfg.py'
config.JobType.numCores = 1
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = True
#config.Data.publication = False

config.section_('Site')
config.Data.ignoreLocality = True
#config.Site.whitelist = ['T1_US_*','T2_US_*', 'T2_CH_CERN']
config.Site.whitelist = ['T2_CH_CERN']
config.Site.storageSite = 'T2_CH_CERN'
#config.Site.storageSite = 'T2_US_MIT'
#config.Site.storageSite = 'T3_US_Rice'

def submit(config):
    try:
        crabCommand('submit', config = config, dryrun=False)
    except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
    except ClientException as cle:
        print "Failed submitting task: %s" % (cle)

#############################################################################################
## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
#############################################################################################

dataMap = {
#        "STARlight_CohJpsi2MuMu_PbPb5TeV_LHE_GenSim_v1": { "InputFiles": "lheFileList/CohJpsi_lhe.txt", "PrimaryDataset": "STARlight_CohJpsi2MuMu_PbPb5TeV_GenFilter", "Memory": 2000, "RunTime": 1000 },
#        "STARlight_InCohJpsi2MuMu_PbPb5TeV_LHE_GenSim_v1": { "InputFiles": "lheFileList/InCohJpsi_lhe.txt", "PrimaryDataset": "STARlight_InCohJpsi2MuMu_PbPb5TeV_GenFilter", "Memory": 2000, "RunTime": 1000 },
#        "STARlight_CohPsi2SFeeddown2MuMu_PbPb5TeV_LHE_GenSim_v1": { "InputFiles": "lheFileList/CohPsi2SFeeddown_lhe.txt", "PrimaryDataset": "STARlight_CohPsi2SFeeddown2MuMu_PbPb5TeV_GenFilter", "Memory": 2000, "RunTime": 1000 },
#        "STARlight_CohPsi2S2MuMu_PbPb5TeV_LHE_GenSim_v1": { "InputFiles": "lheFileList/CohPsi2S_lhe.txt", "PrimaryDataset": "STARlight_CohPsi2S2MuMu_PbPb5TeV_GenFilter", "Memory": 2000, "RunTime": 1000 },
#        "STARlight_InCohPsi2S2MuMu_PbPb5TeV_LHE_GenSim_v1": { "InputFiles": "lheFileList/InCohPsi2S_lhe.txt", "PrimaryDataset": "STARlight_InCohPsi2S2MuMu_PbPb5TeV_GenFilter", "Memory": 2000, "RunTime": 1000 },
#        "STARlight_LowMassGammaGamma2MuMu_PbPb5TeV_LHE_GenSim_v1": { "InputFiles": "lheFileList/LowMassGammaGamma_lhe.txt", "PrimaryDataset": "STARlight_LowMassGammaGamma2MuMu_PbPb5TeV_GenFilter", "Memory": 2000, "RunTime": 1000 },

# Compared to v1 of CohJpsi 0n0n, 0nXn, XnXn, v2 has much more statistics, this is the only difference
        "STARlight_CohJpsi2MuMu_0n0n_PbPb5TeV_LHE_GenSim_v2": { "InputFiles": "lheFileList/CohJpsi_0n0n_lhe.txt", "PrimaryDataset": "STARlight_CohJpsi2MuMu_0n0n_PbPb5TeV_GenFilter", "Memory": 2000, "RunTime": 1000 },
        "STARlight_CohJpsi2MuMu_0nXn_PbPb5TeV_LHE_GenSim_v2": { "InputFiles": "lheFileList/CohJpsi_0nXn_lhe.txt", "PrimaryDataset": "STARlight_CohJpsi2MuMu_0nXn_PbPb5TeV_GenFilter", "Memory": 2000, "RunTime": 1000 },
        "STARlight_CohJpsi2MuMu_XnXn_PbPb5TeV_LHE_GenSim_v2": { "InputFiles": "lheFileList/CohJpsi_XnXn_lhe.txt", "PrimaryDataset": "STARlight_CohJpsi2MuMu_XnXn_PbPb5TeV_GenFilter", "Memory": 2000, "RunTime": 1000 },
        }

## Submit job for different datasets 
for key, val in dataMap.items():
    config.General.requestName = key
    config.JobType.maxMemoryMB = val["Memory"]
    config.JobType.maxJobRuntimeMin = val["RunTime"]
#    config.Data.inputDataset = val["Dataset"]
    config.Data.userInputFiles = open(val["InputFiles"]).readlines() 
    config.Data.outputPrimaryDataset = val["PrimaryDataset"]
    config.Data.outputDatasetTag = config.General.requestName
#    config.Data.outLFNDirBase = '/store/user/shuaiy/RiceHIN/STARlight/%s' %  config.General.requestName
    config.Data.outLFNDirBase = '/store/group/phys_heavyions/shuaiy/STARlight/GenSim/%s' %  config.General.requestName
    print("Submitting CRAB job for: "+val["InputFiles"])
    submit(config)
