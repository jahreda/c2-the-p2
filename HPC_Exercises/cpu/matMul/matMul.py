# Uncomment the following import if you have Numba installed.
from numba import jit, prange
import numpy as np
import time
def matmul_naive(A, B):
    """
    Naive matrix multiplication with triple nested loops.
    Computes C = A * B for matrices A and B.
    """
    n, m = A.shape
    m, p = B.shape
    C = np.zeros((n, p))
    # Triple loop for matrix multiplication
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
    m, p = B.shape
    C = np.zeros((n, p))
    for i in prange(n):
        for j in range(p):
            temp = 0.0
            for k in range(m):
                temp += A[i, k] * B[k, j]
            C[i, j] = temp
    return C

def main():
    # Matrix dimension (feel free to adjust this value)
    n = 500  # For very large sizes, the naive version may become very slow.

    # Generate two random matrices A and B
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)

    # --- Naive Python Matrix Multiplication ---
    start_time = time.time()
    C_naive = matmul_naive(A, B)
    naive_time = time.time() - start_time
    print("Naive Python matrix multiplication time: {:.4f} sec".format(naive_time))

    # --- Numba Accelerated Matrix Multiplication ---
    # Run once to compile the function before timing for a fair comparison.
    matmul_numba(A, B)
    start_time = time.time()
    C_numba = matmul_numba(A, B)
    numba_time = time.time() - start_time
    print("Numba parallel matrix multiplication time: {:.4f} sec".format(numba_time))


if __name__ == "__main__":
    main() 
