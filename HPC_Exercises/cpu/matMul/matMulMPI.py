from mpi4py import MPI
from numba import jit, prange
import numpy as np
import time
import argparse

def matmul_naive(A, B):
    """
    Naive matrix multiplication with triple nested loops.
    Computes C = A * B for the given matrices A and B.
    """
    n, m = A.shape
    m2, p = B.shape
    if m != m2:
        raise ValueError("Inner dimensions do not match.")
    C = np.zeros((n, p))
    for i in range(n):
        for j in range(p):
            for k in range(m):
                C[i, j] += A[i, k] * B[k, j]
    return C

@jit(nopython=True, parallel=True)
def matmul_numba(A, B):
    """
    Matrix multiplication accelerated by Numba with parallelization.
    Uses prange for parallel looping over the outer dimension.
    """
    n, m = A.shape
    m2, p = B.shape
    if m != m2:
        raise ValueError("Inner dimensions do not match.")
    C = np.zeros((n, p))
    for i in prange(n):
        for j in range(p):
            temp = 0.0
            for k in range(m):
                temp += A[i, k] * B[k, j]
            C[i, j] = temp
    return C

def main():
    parser = argparse.ArgumentParser(description="Distributed matrix multiplication with MPI")
    parser.add_argument(
        "--no-naive",
        action="store_true",
        help="Skip the naive triple-loop multiplication entirely"
    )
    parser.add_argument(
        "-n", type=int, default=1000,
        help="Matrix dimension (n x n). Default: 1000"
    )
    args = parser.parse_args()

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    n = args.n

    if rank == 0:
        print("Generating matrices on rank 0 ...")
        A_full = np.random.rand(n, n)
        B_full = np.random.rand(n, n)
        A_parts = np.array_split(A_full, size, axis=0)
    else:
        B_full = None
        A_parts = None

    B = comm.bcast(B_full, root=0)
    A_local = comm.scatter(A_parts, root=0)

    if not args.no_naive:
        t_start_naive = MPI.Wtime()
        C_local_naive = matmul_naive(A_local, B)
        t_end_naive = MPI.Wtime()
        local_time_naive = t_end_naive - t_start_naive
        C_naive_parts = comm.gather(C_local_naive, root=0)
        global_time_naive = comm.reduce(local_time_naive, op=MPI.MAX, root=0)
    else:
        comm.gather(None, root=0)
        global_time_naive = None

    _ = matmul_numba(A_local, B)  
    t_start_numba = MPI.Wtime()
    C_local_numba = matmul_numba(A_local, B)
    t_end_numba = MPI.Wtime()
    local_time_numba = t_end_numba - t_start_numba
    C_numba_parts = comm.gather(C_local_numba, root=0)
    global_time_numba = comm.reduce(local_time_numba, op=MPI.MAX, root=0)

    if rank == 0:
        if not args.no_naive:
            C_naive = np.vstack(C_naive_parts)
        C_numba = np.vstack(C_numba_parts)

        print(f"Distributed matrix multiplication complete on {size} processes.")
        if not args.no_naive:
            print(f"Naive distributed multiplication time (max over nodes): {global_time_naive:.4f} sec")
        else:
            print("Naive multiplication skipped.")
        print(f"Numba distributed multiplication time (max over nodes): {global_time_numba:.4f} sec")


if __name__ == "__main__":
    main()

