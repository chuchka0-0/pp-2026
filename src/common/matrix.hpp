#pragma once

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <stdexcept>
#include <string>
#include <vector>

struct Matrix
{
    std::int64_t n;
    std::vector<double> a;
    explicit Matrix(std::int64_t size = 0) : n(size), a(size * size, 0.0) {}
};

inline Matrix read_matrix(const std::string &path)
{
    FILE *f = std::fopen(path.c_str(), "rb");
    if (!f)
        throw std::runtime_error("cannot open " + path);
    std::int64_t n = 0;
    bool ok = std::fread(&n, sizeof n, 1, f) == 1 && n > 0;
    Matrix m(ok ? n : 0);
    ok = ok && std::fread(m.a.data(), sizeof(double), m.a.size(), f) == m.a.size();
    std::fclose(f);
    if (!ok)
        throw std::runtime_error("bad matrix file " + path);
    return m;
}

inline void write_matrix(const std::string &path, const Matrix &m)
{
    FILE *f = std::fopen(path.c_str(), "wb");
    if (!f)
        throw std::runtime_error("cannot write " + path);
    bool ok = std::fwrite(&m.n, sizeof m.n, 1, f) == 1 &&
              std::fwrite(m.a.data(), sizeof(double), m.a.size(), f) == m.a.size();
    std::fclose(f);
    if (!ok)
        throw std::runtime_error("write failed " + path);
}

inline void multiply(const double *A, const double *B, double *C, std::int64_t n, std::int64_t rows)
{
    for (std::int64_t i = 0; i < rows; ++i)
    {
        double *c = C + i * n;
        std::fill(c, c + n, 0.0);
        for (std::int64_t k = 0; k < n; ++k)
        {
            const double aik = A[i * n + k];
            const double *b = B + k * n;
            for (std::int64_t j = 0; j < n; ++j)
                c[j] += aik * b[j];
        }
    }
}

inline double now_seconds()
{
    using namespace std::chrono;
    return duration<double>(steady_clock::now().time_since_epoch()).count();
}

inline void print_result(const char *lab, std::int64_t n, int workers, double seconds)
{
    const double ops = 2.0 * n * n * n;
    std::printf("%s,%lld,%d,%.6f,%.0f,%.3f\n", lab, static_cast<long long>(n), workers,
                seconds, ops, ops / seconds * 1e-9);
}
