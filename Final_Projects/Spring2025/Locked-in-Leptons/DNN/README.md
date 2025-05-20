`DNN.ipynb`: Analysis that closely follow part 1 of the hls4ml tutorial. Creates a Keras ML model that is stored in a model\_1/ file and converts Keras model to hls using hls4ml. No optimization was done to the hls model. A comparison of the ROC curves for both were done and can be found in `AUC.png`. An output of the vivado report is shown aswell. 

`Opt_*layer.ipynb`: Each notebook closely follows part 2 of the hls4ml tutorial. The model saved from `DNN.ipynb` is loaded and then converted to hls using hls4ml. 1 corresponds to optimizing the weights for the first hidden layer, 2 to optimizing both 1st and 2nd layer, and 3 to optimizing all layers. Each ROC curve was plotted in comparison to the original Keras model and can be found in `ROC_*layer.png`. 

`callback.py`: Is a copy from hls4ml tutorial which saves the original Keras model to an output file. 

`plotting.py`: Is also a copy from hls4ml tutorial that helps plot ROC curves. 

Due to limited disk space in vmlab. I recommend killing any gpu processes and reseting kernals before running each notebook. 
