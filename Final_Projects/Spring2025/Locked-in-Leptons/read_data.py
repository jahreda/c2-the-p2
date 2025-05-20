import uproot
import numpy as np

##### 1 lep
#W+ datasets
Wplusenu_data_1l = uproot.open("https://atlas-opendata.web.cern.ch/Legacy13TeV/1lep/MC/mc_361100.Wplusenu.1lep.root")
#W- datasets
Wminusenu_data_1l = uproot.open("https://atlas-opendata.web.cern.ch/Legacy13TeV/1lep/MC/mc_361103.Wminusenu.1lep.root")

##### 2 lep
#W+ datasets
Wplusenu_data_2l = uproot.open("https://atlas-opendata.web.cern.ch/Legacy13TeV/2lep/MC/mc_361100.Wplusenu.2lep.root")
#W- datasets
Wminusenu_data_2l = uproot.open("https://atlas-opendata.web.cern.ch/Legacy13TeV/2lep/MC/mc_361103.Wminusenu.2lep.root")

##### 1 lep
Zee_data_1l = uproot.open("https://atlas-opendata.web.cern.ch/Legacy13TeV/1lep/MC/mc_361106.Zee.1lep.root")
# Zmumu_data_1l = uproot.open("https://atlas-opendata.web.cern.ch/Legacy13TeV/1lep/MC/mc_361107.Zmumu.1lep.root")
# Ztautau_data_1l = uproot.open("https://atlas-opendata.web.cern.ch/Legacy13TeV/1lep/MC/mc_361108.Ztautau.1lep.root")

##### 2 lep
Zee_data_2l = uproot.open("https://atlas-opendata.web.cern.ch/Legacy13TeV/2lep/MC/mc_361106.Zee.2lep.root")
# Zmumu_data_2l = uproot.open("https://atlas-opendata.web.cern.ch/Legacy13TeV/2lep/MC/mc_361107.Zmumu.2lep.root")
# Ztautau_data_2l = uproot.open("https://atlas-opendata.web.cern.ch/Legacy13TeV/2lep/MC/mc_361108.Ztautau.2lep.root")


import awkward as ak
features = ["met_et", "met_phi", "jet_pt", "jet_eta", "jet_phi", "lep_pt", "lep_phi", "lep_eta"]
W_data = ak.concatenate([Wplusenu_data_1l['mini'].arrays(features),
                         Wplusenu_data_2l['mini'].arrays(features),
                        ])


Z_data = ak.concatenate([Zee_data_1l['mini'].arrays(features),
#                         Zmumu_data_1l['mini'].arrays(features),
#                         Ztautau_data_1l['mini'].arrays(features),
                         Zee_data_2l['mini'].arrays(features),
#                         Zmumu_data_2l['mini'].arrays(features),
#                         Ztautau_data_2l['mini'].arrays(features)
])

import os
try:
    os.mkdir("data")
except:
    pass

ak.to_parquet(W_data, "data/W_data.parquet")
ak.to_parquet(Z_data, "data/Z_data.parquet")

