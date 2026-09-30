#pragma once

#include <chrono>
#include <cstdio>
#include <stdexcept>
#include <string>
#include <vector>

typedef long long Value;

struct Matrix
{
    int n;
    std::vector<Value> a;
    explicit Matrix(int size = 0) : n(size), a((size_t)size * size, 0) {}
};

inline Matrix read_matrix(const std::string &path)
{
    FILE *f = std::fopen(path.c_str(), "r");
    if (!f)
        throw std::runtime_error("cannot open " + path);
    int n = 0;
    if (std::fscanf(f, "%d", &n) != 1 || n <= 0)
    {
        std::fclose(f);
        throw std::runtime_error("bad file " + path);
    }
    Matrix m(n);
    for (size_t i = 0; i < m.a.size(); ++i)
        if (std::fscanf(f, "%lld", &m.a[i]) != 1)
        {
            std::fclose(f);
            throw std::runtime_error("bad file " + path);
        }
    std::fclose(f);
    return m;
}

inline void write_matrix(const std::string &path, const Matrix &m)
{
    FILE *f = std::fopen(path.c_str(), "w");
    if (!f)
        throw std::runtime_error("cannot write " + path);
    std::fprintf(f, "%d\n", m.n);
    for (int i = 0; i < m.n; ++i)
        for (int j = 0; j < m.n; ++j)
            std::fprintf(f, "%lld%c", m.a[(size_t)i * m.n + j], j + 1 < m.n ? ' ' : '\n');
    std::fclose(f);
}

inline void multiply(const Value *A, const Value *B, Value *C, int n, int rows)
{
    for (int i = 0; i < rows; ++i)
    {
        Value *c = C + (size_t)i * n;
        for (int j = 0; j < n; ++j)
            c[j] = 0;
        for (int k = 0; k < n; ++k)
        {
            const Value aik = A[(size_t)i * n + k];
            const Value *b = B + (size_t)k * n;
            for (int j = 0; j < n; ++j)
                c[j] += aik * b[j];
        }
    }
}

inline double now_seconds()
{
    using namespace std::chrono;
    return duration<double>(steady_clock::now().time_since_epoch()).count();
}

inline void print_result(const char *lab, int n, int workers, double seconds)
{
    const double ops = 2.0 * n * n * n;
    std::printf("%s,%d,%d,%.6f,%.0f,%.3f\n", lab, n, workers, seconds, ops, ops / seconds * 1e-9);
}
