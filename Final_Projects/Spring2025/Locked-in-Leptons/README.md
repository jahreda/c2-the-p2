# Locked-in-Leptons
Final Project for C2-THE-P2 Course, Spring 2025 : https://github.com/jahreda/c2-the-p2

The objective of this project is to train a ML model to identify events with true MET and program this MET tagger to an FPGA. This project follows closely the [hls4ml tutorial](https://github.com/fastmachinelearning/hls4ml-tutorial). Two applications were done using a BDT and DNN.  

`Presentation.pdf`: Goes into into details behind our motives, analysis, and results. 

`read_data.py`: Script that loads open ATALS data and outputs two parquet files: W_data.parquet and Z_data.parquet.

`data_train_test_split.py`: Script that splits W and Z data parquet files into a training and testing set which is saved as a `.npy` file.

`DNN`: Contains analysis done for DNN application.

`BDT`: Contains analysis done for BDT application.

`environment.yml`: Environment created for hls4ml tutorial.

`Analysis.ipynb`:  Jupyter notebook that analyzes resource usage from optimizing DNN layers and compares resource usage with BDT model. 

`fatimas_results.txt`: Resource usage for each model with different number of optimized layers. Data pulled from vivado reports in notebook `DNN/Opt_*.ipynb` and `DNN.ipynb`.

`franks_results.txt`: Resource usage for different precision settings of the BDT model.
 

## Set-Up
First sign into vmlab and clone this repository. 
```
ssh $USER@vmlab.niu.edu
git clone https://github.com/fatimargz/Locked-in-Leptons.git 
```

Create a conda environment from the environment.yml file 
```
conda env create -f environment.yml
```

Activate the new environment: 
```
conda activate hls4ml-tutorial
```

Source vitis:
```
source /opt/metis/el8/contrib/amdtools/xilinx-2023.1/Vitis/2023.1/settings64.sh
```

Begin port forwarding a jupyter notebook: 
```
jupyter lab --no-browser --port 8080
```

In a separate terminal, connect to the vmlab with the port used above for jupyter lab. Replace `$USER` with your username.
```
ssh -L 8080:local:host:8080 $USER@vmlab.niu.edu
```

## Loading Data
Run the following to load the dataset. It should create two parquet files, W_data.parquet and Z_data.parquet, saved in a new directory `./data`:
```
python read_data.py
```

Then run
```
python data_train_test_split.py
```
to output the training and testing sets to a `.npy` file in `./data`. 
