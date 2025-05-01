#!/bin/bash -l
#PBS -N AFFINITY
#PBS -l select=1:system=crux
#PBS -l place=scatter
#PBS -l walltime=0:10:00
#PBS -q debug
#PBS -A C2theP2
#PBS -l filesystems=home:eagle
#PBS -o logs/matMul.out
#PBS -e logs/matMul.err

# MPI+OpenMP example w/ 64 MPI ranks per node and threads spread evenly across cores
# There are two 32-core CPUs on each node. This will run 32 MPI ranks per CPU, 2 OpenMP threads per rank, and each thread bound to a single core.
. ~/c2p2/bin/activate
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=64 # Number of MPI ranks to spawn per node
NDEPTH=2 # Number of hardware threads per rank (i.e. spacing between MPI ranks)
NTHREADS=2 # Number of software threads per rank to launch (i.e. OMP_NUM_THREADS)

NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE} THREADS_PER_RANK= ${NTHREADS}"

# Change the directory to work directory, which is the directory you submit the job.
cd $PBS_O_WORKDIR

MPI_ARGS="-n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} --depth=${NDEPTH} --cpu-bind depth "
OMP_ARGS="--env OMP_NUM_THREADS=${NTHREADS} --env OMP_PROC_BIND=true --env OMP_PLACES=cores "

mpiexec ${MPI_ARGS} ${OMP_ARGS} python matMul.py
