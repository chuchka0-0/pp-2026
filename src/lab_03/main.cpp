#include <mpi.h>

#include "matrix.hpp"

int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);
    int rank = 0, size = 1;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    if (argc != 4)
    {
        if (rank == 0)
            std::fprintf(stderr, "usage: mpirun -np P %s A.txt B.txt C.txt\n", argv[0]);
        MPI_Finalize();
        return 1;
    }

    Matrix A, B;
    int n = 0;
    if (rank == 0)
    {
        try
        {
            A = read_matrix(argv[1]);
            B = read_matrix(argv[2]);
        }
        catch (const std::exception &e)
        {
            std::fprintf(stderr, "error: %s\n", e.what());
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        if (A.n != B.n)
        {
            std::fprintf(stderr, "error: sizes differ\n");
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        n = A.n;
    }
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
    if (rank != 0)
        B = Matrix(n);

    std::vector<int> counts(size), displs(size);
    for (int r = 0, row = 0; r < size; ++r)
    {
        const int rows = n / size + (r < n % size ? 1 : 0);
        counts[r] = rows * n;
        displs[r] = row * n;
        row += rows;
    }
    std::vector<Value> a(counts[rank]), c(counts[rank]);
    Matrix C(rank == 0 ? n : 0);

    MPI_Barrier(MPI_COMM_WORLD);
    const double t0 = MPI_Wtime();
    MPI_Scatterv(A.a.data(), counts.data(), displs.data(), MPI_LONG_LONG,
                 a.data(), counts[rank], MPI_LONG_LONG, 0, MPI_COMM_WORLD);
    MPI_Bcast(B.a.data(), n * n, MPI_LONG_LONG, 0, MPI_COMM_WORLD);
    multiply(a.data(), B.a.data(), c.data(), n, counts[rank] / n);
    MPI_Gatherv(c.data(), counts[rank], MPI_LONG_LONG,
                C.a.data(), counts.data(), displs.data(), MPI_LONG_LONG, 0, MPI_COMM_WORLD);
    const double t = MPI_Wtime() - t0;

    if (rank == 0)
    {
        try
        {
            write_matrix(argv[3], C);
        }
        catch (const std::exception &e)
        {
            std::fprintf(stderr, "error: %s\n", e.what());
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        print_result("lab_03", n, size, t);
    }
    MPI_Finalize();
    return 0;
}
