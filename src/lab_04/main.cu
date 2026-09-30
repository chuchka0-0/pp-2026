#include "matrix.hpp"

#include <cstdlib>

#include <cuda_runtime.h>

#define CUDA_CHECK(call)                                       \
    do                                                         \
    {                                                          \
        const cudaError_t err = (call);                        \
        if (err != cudaSuccess)                                \
            throw std::runtime_error(cudaGetErrorString(err)); \
    } while (0)

__global__ void multiply_kernel(const Value *A, const Value *B, Value *C, int n)
{
    const int i = blockIdx.y * blockDim.y + threadIdx.y;
    const int j = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n || j >= n)
        return;
    Value sum = 0;
    for (int k = 0; k < n; ++k)
        sum += A[i * n + k] * B[k * n + j];
    C[i * n + j] = sum;
}

int main(int argc, char **argv)
{
    if (argc != 4)
    {
        std::fprintf(stderr, "usage: BLOCK_SIZE=16 %s A.txt B.txt C.txt\n", argv[0]);
        return 1;
    }
    try
    {
        const Matrix A = read_matrix(argv[1]);
        const Matrix B = read_matrix(argv[2]);
        if (A.n != B.n)
            throw std::runtime_error("matrix sizes differ");
        const char *env = std::getenv("BLOCK_SIZE");
        const int block = env ? std::atoi(env) : 16;
        if (block < 1 || block > 32)
            throw std::runtime_error("BLOCK_SIZE must be in 1..32");

        const int n = A.n;
        const size_t bytes = A.a.size() * sizeof(Value);
        Matrix C(n);
        Value *dA, *dB, *dC;
        CUDA_CHECK(cudaMalloc(&dA, bytes));
        CUDA_CHECK(cudaMalloc(&dB, bytes));
        CUDA_CHECK(cudaMalloc(&dC, bytes));
        CUDA_CHECK(cudaMemcpy(dA, A.a.data(), bytes, cudaMemcpyHostToDevice));
        CUDA_CHECK(cudaMemcpy(dB, B.a.data(), bytes, cudaMemcpyHostToDevice));

        const dim3 threads(block, block);
        const dim3 grid((n + block - 1) / block, (n + block - 1) / block);
        cudaEvent_t start, stop;
        CUDA_CHECK(cudaEventCreate(&start));
        CUDA_CHECK(cudaEventCreate(&stop));

        multiply_kernel<<<grid, threads>>>(dA, dB, dC, n); // прогрев
        CUDA_CHECK(cudaGetLastError());
        CUDA_CHECK(cudaEventRecord(start));
        multiply_kernel<<<grid, threads>>>(dA, dB, dC, n);
        CUDA_CHECK(cudaGetLastError());
        CUDA_CHECK(cudaEventRecord(stop));
        CUDA_CHECK(cudaEventSynchronize(stop));
        float ms = 0.0f;
        CUDA_CHECK(cudaEventElapsedTime(&ms, start, stop));

        CUDA_CHECK(cudaMemcpy(C.a.data(), dC, bytes, cudaMemcpyDeviceToHost));
        cudaFree(dA);
        cudaFree(dB);
        cudaFree(dC);

        write_matrix(argv[3], C);
        print_result("lab_04", n, block, ms * 1e-3);
    }
    catch (const std::exception &e)
    {
        std::fprintf(stderr, "error: %s\n", e.what());
        return 1;
    }
    return 0;
}
