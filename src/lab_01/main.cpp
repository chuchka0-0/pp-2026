#include "matrix.hpp"

#include <exception>

int main(int argc, char **argv)
{
    if (argc != 4)
    {
        std::fprintf(stderr, "usage: %s A.bin B.bin C.bin\n", argv[0]);
        return 1;
    }
    try
    {
        const Matrix A = read_matrix(argv[1]);
        const Matrix B = read_matrix(argv[2]);
        if (A.n != B.n)
            throw std::runtime_error("matrix sizes differ");

        Matrix C(A.n);
        const double t0 = now_seconds();
        multiply(A.a.data(), B.a.data(), C.a.data(), A.n, A.n);
        const double t = now_seconds() - t0;

        write_matrix(argv[3], C);
        print_result("lab_01", A.n, 1, t);
    }
    catch (const std::exception &e)
    {
        std::fprintf(stderr, "error: %s\n", e.what());
        return 1;
    }
    return 0;
}
