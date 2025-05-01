

# Using PBS on Sophia

![image](https://github.com/user-attachments/assets/0d020781-322b-4a5b-b115-c0531904e16e)

we will be running jobs using 1 gpu. If enough nodes are open, we can try running by node. 

```
qsub <file> submits a batch job
qstat -u $USEr check the status of your jobs
qstat` check the status of ALL jobs on the system
qdel <job number> deletes job

```
## Matrix Multiplication on GPU
### Install packages:
make logs folder: mkdir logs

```
module use /soft/modulefiles; module load conda; conda activate base

VENV_DIR="$(pwd)/venvs/c2p2"

mkdir -p "${VENV_DIR}"

python -m venv "${VENV_DIR}" --system-site-packages

source /home/anrunw/C2theP2ExerciseHPC/gpu/matMul/venvs/c2p2/bin/activate


pip install numba

pip install pycuda



```

### Run matrix multiplication matrix on GPU

run `runMatMulGPU.sh` using qsub 

check performance in logs, and play around with different sizes of matrices. 
