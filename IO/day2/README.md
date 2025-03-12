The unit tests dealt with here are specific for some of the core I/O functionality that are tested whenever a new build (nightly or merged) of Athena is produced.

Below is the contents of the file called `athena` in the repo:  

```bash
### this runs on the UChicago AF

mkdir traineeship
cd traineeship
setupATLAS
lsetup git
git atlas init-workdir https://:@gitlab.cern.ch:8443/jahreda/athena.git
cd athena
git atlas addpkg AthenaPoolExample
cd ..
mkdir build
cd build
asetup Athena,main,latest
cmake ../athena/Projects/WorkDir/
make
source x86_64-el9-gcc13-opt/setup.sh
cd ..
mkdir run
cd run/

### run
python -m AthenaPoolExampleAlgorithms.AthenaPoolExample_Write.py >& log0
python -m AthenaPoolExampleAlgorithms.AthenaPoolExample_ReadWrite.py >& log1
python -m AthenaPoolExampleAlgorithms.AthenaPoolExample_ReadWriteNext.py > log2
python -m AthenaPoolExampleAlgorithms.AthenaPoolExample_WritexAODElectrons.py >& log3
python -m AthenaPoolExampleAlgorithms.AthenaPoolExample_ReadxAODElectrons.py >& log4


### if you log in again you only need to do this before running again:
cd traineeship
setupATLAS
cd build
asetup Athena,main,latest
source x86_64-el9-gcc13-opt/setup.sh
cd ../run

### View inside SimplePoolFile_xAOD.root
checkxAOD SimplePoolFile_xAOD.root

### To view all of the branches stored file
checkFile SimplePoolFile_xAOD.root

```


This shows you how to setup a working environment, run the unit tests apart of the `AthenaPoolExample` package. I've put together something of an exercise that illustrates the steps needed to be taken if one wanted to modify the unit tests.

Before moving ahead, feel free to login to the UChicago Analysis Facility (or if you have a CERN Grid node and are more comfortable with that), navigate to your desired work directory and copy and paste the commands up until `### run`.  This should take a minute or so, and assuming no errors you should be in a `/run/` directory. Here you can run the `AthenaPoolExample_Write.py` script with `log0` as the text output. 

If you like, before proceeding, you can take a look at the output of `log0` and look around using the `checkxAOD` and `checkFile` commands. Once satisfied, you can proceed to run the rest of the scripts. 

How does this work? A Python script is used at a high-level to configure or steer a job, in this case our unit tests. A typical script has job flags, establishes a main component accumulator service, sets up which Algorithms to execute for each event, configures output streams, and more. By using flags, a user can define things like the input/output ROOT file, the maximum number of events iterated, debug messaging, etc. An Algorithm can take in some event data and process it however it needs to and when it's done it will write to file. More info can be found here in the [docs](https://atlassoftwaredocs.web.cern.ch/athena/configuration/)


---
## Some exposition: 

Initially we run through, in order, 
```bash
AthenaPoolExample_Write.py 
AthenaPoolExample_ReadWrite.py
AthenaPoolExample_ReadWriteNext.py
```
 because it's these unit-tests that process TestHits and create TestTracks so that `WritexAODElectrons` can loop through each track per event. After running `AthenaPoolExample_ReadWriteNext.py` we have Track objects in `SimplePoolFile3.root` which allows us to access it in the python script as a flag
```
flags.Input.Files = ["SimplePoolFile3.root"]
```



---
## Modifying the tests

Path to write algorithms
```bash
athena/Database/AthenaPOOL/AthenaPoolExample/AthenaPoolExampleAlgorithms/src
```

In the `WriteExampleElectron.h`: 
Add two more decorations, one for floats(4 bytes) and one for long double (8-10 byes)? 
```c++
  SG::WriteDecorHandleKey<xAOD::ExampleElectronContainer> m_decor_floatKey{
      this, "ExampleElectronContainerDecorKeyFloat", "TestContainer.decor_float",
      "decorator for float key"};

  SG::WriteDecorHandleKey<xAOD::ExampleElectronContainer> m_decor_longdoubleKey{
      this, "ExampleElectronContainerDecorKeyLongDouble", "TestContainer.decor_longdouble",
      "decorator for long double key"};
```

In the `WriteExampleElectron.cxx`:
We'll need to do something with these keys..

First in `::initalize()`
Initialize the keys
```
  ATH_CHECK(m_decor_floatKey.initialize());
  ATH_CHECK(m_decor_longdoubleKey.initialize());
```

then in the `::execute()`
You'll need a handle to open the object/decoration ( with the key inserted )
```
<< check context in WriteExampleElectron.cpp >>
```

Then you can start assigning your handle with values 
```
<< check context in WriteExampleElectron.cpp >>
```

---
## Building

When you want to build the changes you've made you can go back to the build `/traineeship/build/` directory and run
```bash
make -j4
```

navigating to `/run/`, what goes wrong with the python script? 

The log reveals that 
```
AthenaPoolCnvSvc                                    DEBUG setAttribute TREE_MAX_SIZE to 1099511627776L
AthenaPoolCnvSvc                                    DEBUG setAttribute DEFAULT_SPLITLEVEL to 0
AthenaPoolCnvSvc                                    DEBUG setAttribute STREAM_MEMBER_WISE to 1
AthenaPoolCnvSvc                                    DEBUG setAttribute DEFAULT_BUFFERSIZE to 32000
AthenaPoolCnvSvc                                    DEBUG setAttribute TREE_BRANCH_OFFSETTAB_LEN to 100
```
```
CollectionTree(TestContainerAux.)                   ERROR Dynamic attributes writing error: Failed to create Auxiliary branch 'TestContainerAuxDyn.decor_longdouble'. Class: std::vector<long double>
```
and that
```
CollectionTree(TestContainerAux.)                   ERROR Dynamic attributes writing error: Failed to create Auxiliary branch 'TestContainerAuxDyn.decor_longdouble'. Class: std::vector<long double>
```

### So how can you fix this? 

Go into `/python/AthenaPoolExample_WritexAODElectrons.py`
change the following line into 
```
"xAOD::ExampleElectronAuxContainer#TestContainerAux.-decor2"] )
```
into
```
<< what do you think should go here? >>
```


### With all of this in mind, how can you get the Algorithm `ReadExampleElectron` to read through decorations?

---

## Another exercise: Write multiple electrons per track

Currently `WriteExampleElectron.cxx` loops over all of the tracks in the event, but there's really only one per event in these unit tests. 
