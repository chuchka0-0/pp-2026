#include "matrix.hpp"

#include <omp.h>

int main(int argc, char **argv)
{
    if (argc != 4)
    {
        std::fprintf(stderr, "usage: %s A.txt B.txt C.txt\n", argv[0]);
        return 1;
    }
    try
    {
        const Matrix A = read_matrix(argv[1]);
        const Matrix B = read_matrix(argv[2]);
        if (A.n != B.n)
            throw std::runtime_error("matrix sizes differ");

        const int n = A.n;
        Matrix C(n);
        const int threads = omp_get_max_threads();

        const double t0 = now_seconds();
#pragma omp parallel for schedule(static)
        for (int i = 0; i < n; ++i)
            multiply(A.a.data() + (size_t)i * n, B.a.data(), C.a.data() + (size_t)i * n, n, 1);
        const double t = now_seconds() - t0;

        write_matrix(argv[3], C);
        print_result("lab_02", n, threads, t);
    }
    catch (const std::exception &e)
    {
        std::fprintf(stderr, "error: %s\n", e.what());
        return 1;
    }
    return 0;
}
