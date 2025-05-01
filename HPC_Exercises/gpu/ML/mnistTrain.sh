#!/bin/bash -l
#PBS -l select=1:system=sophia
#PBS -l place=scatter
#PBS -l walltime=0:05:00
#PBS -q by-gpu
#PBS -A C2theP2
#PBS -l filesystems=home:grand:eagle

# Log output and error files
#PBS -o logs/mnist.out
#PBS -e logs/mnist.err

cd ${PBS_O_WORKDIR}
module use /soft/modulefiles; module load conda; conda activate base
NNODES=$(wc -l < $PBS_NODEFILE)
NRANKS_PER_NODE=2
NDEPTH=64
NTHREADS=64

NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE} THREADS_PER_RANK= ${NTHREADS}"

# Define MPI parameters
MPI_ARG="-n ${NTOTRANKS} --npernode ${NRANKS_PER_NODE} "
MPI_ARG+=" -x OMP_NUM_THREADS=${NTHREADS} -x OMP_PROC_BIND=spread -x OMP_PLACES=cores "

# Run the Python script using mpiexec
mpiexec ${MPI_ARG} python mnist.py
