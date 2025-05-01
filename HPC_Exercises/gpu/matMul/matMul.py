import numpy as np
import math
import time

import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

# CUDA kernel code for matrix multiplication.
kernel_code = """
__global__ void matmul(const float* A, const float* B, float* C, int n) {
    // Calculate the row index of the C element and A.
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    // Calculate the column index of the C element and B.
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    
    // Only perform multiplication if within bounds.
    if (row < n && col < n) {
        float sum = 0.0f;
        // Loop over the shared dimension.
        for (int k = 0; k < n; k++) {
            sum += A[row * n + k] * B[k * n + col];
        }
        C[row * n + col] = sum;
    }
}
"""

# Compile the CUDA kernel.
mod = SourceModule(kernel_code)
matmul = mod.get_function("matmul")

def main():
    # Matrix dimension; you can adjust this value as needed.
    n = 1000

    # Create two random matrices A and B (as float32 arrays for CUDA).
    A = np.random.rand(n, n).astype(np.float32)
    B = np.random.rand(n, n).astype(np.float32)
    C = np.zeros((n, n), dtype=np.float32)

    # Allocate device memory for A, B, and C.
    d_A = cuda.mem_alloc(A.nbytes)
    d_B = cuda.mem_alloc(B.nbytes)
    d_C = cuda.mem_alloc(C.nbytes)

    # Copy host data (A, B) to the device memory.
    cuda.memcpy_htod(d_A, A)
    cuda.memcpy_htod(d_B, B)

    # Define the block size. A common choice is (16, 16).
    block_size = (16, 16, 1)
    # Calculate grid dimensions to cover the whole matrix.
    grid_size_x = math.ceil(n / block_size[0])
    grid_size_y = math.ceil(n / block_size[1])
    grid_size = (grid_size_x, grid_size_y, 1)

    # Start the timer.
    start = time.time()
    # Launch the kernel.
    # We pass d_A, d_B, d_C and the matrix dimension as an int32.
    matmul(d_A, d_B, d_C, np.int32(n), block=block_size, grid=grid_size)
    # Wait for the kernel to finish.
    cuda.Context.synchronize()
    elapsed = time.time() - start

    print("GPU matrix multiplication time: {:.4f} sec".format(elapsed))

    # Copy the result from device to host.
    cuda.memcpy_dtoh(C, d_C)

    # Optional: Verify result against NumPy's dot product.
    C_np = np.matmul(A, B)

if __name__ == '__main__':
    main()

