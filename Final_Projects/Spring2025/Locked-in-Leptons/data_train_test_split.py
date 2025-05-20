import awkward as ak
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np

# Import the parquet files with training data
W_data = ak.from_parquet("W_data.parquet")
Z_data = ak.from_parquet("Z_data.parquet")

# add labels
W_data["MET"] = len(W_data)*[1]
Z_data["MET"] = len(Z_data)*[0]

# combine and shuffle
combined = ak.concatenate([W_data, Z_data])
combined = combined[ak.argsort(np.random.rand(len(combined)))]

# For events with less than three jets or two leptons, add null placeholders
for field in ["jet_pt", "jet_eta", "jet_phi"]:
    combined = ak.with_field(combined, combined[field][:, :3], field)
    combined[field] = ak.fill_none(ak.pad_none(combined[field],3, axis = 1),0)

for field in ["lep_pt", "lep_eta", "lep_phi"]:
    combined = ak.with_field(combined, combined[field][:, :2], field)
    combined[field] = ak.fill_none(ak.pad_none(combined[field],2, axis = 1),0)

# Separate into training and testing sets
indices = np.arange(len(combined))
train_idx, test_idx = train_test_split(indices, stratify=combined["MET"], test_size = 0.3)
train = combined[train_idx]
test = combined[test_idx]


y_train = ak.to_numpy(train["MET"])
y_test = ak.to_numpy(test["MET"])

x_train = np.stack([
    ak.to_numpy(train["jet_pt"][:, 0]),
    ak.to_numpy(train["jet_eta"][:, 0]),
    ak.to_numpy(train["jet_phi"][:, 0]),
    ak.to_numpy(train["jet_pt"][:, 1]),
    ak.to_numpy(train["jet_eta"][:, 1]),
    ak.to_numpy(train["jet_phi"][:, 1]),
    ak.to_numpy(train["jet_pt"][:, 2]),
    ak.to_numpy(train["jet_eta"][:, 2]),
    ak.to_numpy(train["jet_phi"][:, 2]),
    ak.to_numpy(train["lep_pt"][:, 0]),
    ak.to_numpy(train["lep_eta"][:, 0]),
    ak.to_numpy(train["lep_phi"][:, 0]),
    ak.to_numpy(train["lep_pt"][:, 1]),
    ak.to_numpy(train["lep_eta"][:, 1]),
    ak.to_numpy(train["lep_phi"][:, 1]),
    ak.to_numpy(train["met_et"]),
    ak.to_numpy(train["met_phi"])
], axis=1)

x_test = np.stack([
    ak.to_numpy(test["jet_pt"][:, 0]),
    ak.to_numpy(test["jet_eta"][:, 0]),
    ak.to_numpy(test["jet_phi"][:, 0]),
    ak.to_numpy(test["jet_pt"][:, 1]),
    ak.to_numpy(test["jet_eta"][:, 1]),
    ak.to_numpy(test["jet_phi"][:, 1]),
    ak.to_numpy(test["jet_pt"][:, 2]),
    ak.to_numpy(test["jet_eta"][:, 2]),
    ak.to_numpy(test["jet_phi"][:, 2]),
    ak.to_numpy(test["lep_pt"][:, 0]),
    ak.to_numpy(test["lep_eta"][:, 0]),
    ak.to_numpy(test["lep_phi"][:, 0]),
    ak.to_numpy(test["lep_pt"][:, 1]),
    ak.to_numpy(test["lep_eta"][:, 1]),
    ak.to_numpy(test["lep_phi"][:, 1]),
    ak.to_numpy(test["met_et"]),
    ak.to_numpy(test["met_phi"])
], axis=1)

# Save numpy arrays
np.save("x_train.npy", x_train)
np.save("x_test.npy", x_test)
np.save("y_train.npy", y_train)
np.save("y_test.npy", y_test)