
# Using PBS on Crux

![image](https://github.com/user-attachments/assets/845e39b4-02a9-4288-bd2a-3ee8f4c93c1f)

```
qsub <file> submits a batch job
qstat -u $USEr check the status of your jobs
qstat` check the status of ALL jobs on the system
qdel <job number> deletes job

```
## Matrix Multiplication on CPU
### Install packages:
make logs folder: mkdir logs

```
python3 -m venv ~/c2p2

. ~/c2p2/bin/activate

pip install mpi4py

pip install numba

pip install numpy

```

### Run matrix multiplication matrix without parallelization.

edit `runMatMulCPU.sh` to run on 1 node using vim, gromacs... by setting the value after select to 1: `#PBS -l select=1:system=crux`

Run the script: `qsub runMatMulCPU.sh`

Go into logs and look at the `matMul.out` output. Notice how the output is printed multiple times. Why is that?

Now, run it on 4 nodes. Do you expect it to run faster? slower? or the same?

Look at output logs and compare. 


### Run Matrix multiplication with parallelization across CPU nodes

edit `runMatMulMPI.sh` to run on 1 node and submit the job using `qsub runMatMulMPI.sh`. Look at output in logs. 

Now, run it on 4 nodes. Compare the runtime of the matrix multiplications. 

in `runMatMulMPI.sh` you can edit the run script 

`matMulMPI.py --no-naive -n <size of matrices> `  

`--no-naive` parameter disables the naive execution

play around with the size of the matrices and start a job. See how at larger matrix sizes multiplication is still fast, but the naive implementation slows down. Play around with the number of nodes, and see if runtime decreases with number of node. 
