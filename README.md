# Параллельное программирование: умножение квадратных матриц

Лабораторные №1–5: последовательная версия, OpenMP, MPI (суперкомпьютер «Сергей Королёв»), CUDA.
Сейчас реализована **л/р №1** (последовательная версия); остальные подключаются по той же схеме.

## Быстрый старт

```bash
pip install -r requirements.txt
make all                         # build → data → run → verify → plot
make all SIZES="200 400" REPEATS=1   # быстрый прогон
```

Цели по отдельности: `make build`, `make data`, `make run`, `make verify`, `make plot`,
`make clean`, `make clean-results`. Параметры (`LAB`, `SIZES`, `SEED`, `REPEATS`, `PYTHON`)
задаются в командной строке или в `.env` (см. `.env.example`).

## Как это устроено

```
generate.py ──► data/A_n.bin, B_n.bin ──► build/bin/lab_XX ──► results/lab_XX/C_n.bin
   (seed)                                      │ stdout: 1 строка CSV
                                               ▼
                       run.py ──► results/lab_XX/results.csv
                       verify.py (numpy A @ B) ──► results/lab_XX/verification.csv
                       plot.py ──► reports/lab_XX/{time,gflops}.png, summary.csv
```

- **Данные** генерирует `scripts/generate.py`: `RandomState([seed, n])`, значения в [-1, 1).
  Одинаковый seed — одинаковые матрицы для всех лабораторных.
- **Формат матриц** (бинарный, одинаковый в C++ и Python): `int64 n`, затем `n*n` × `float64`, little-endian.
- **Программа** `lab_XX A.bin B.bin C.bin` читает матрицы, замеряет только время умножения,
  пишет `C.bin` и одну строку CSV: `lab,n,workers,time_s,ops,gflops`
  (`ops = 2n³` — объём задачи, `workers` — число потоков/процессов).
- **Верификация**: относительная погрешность `max|C − A@B| / max|A@B| < 1e-10`,
  при ошибке `verify.py` завершается с кодом 1.
- **Графики**: каждая пара `(lab, workers)` — своя линия, по повторам берётся медиана.
  `make plot` рисует все найденные `results/*/results.csv` на одном графике,
  поэтому в следующих лабораторных сразу видно сравнение подходов.

## Структура

```
src/common/matrix.hpp   общее: Matrix, read/write, multiply (по блоку строк), таймер, вывод CSV
src/lab_01/             main.cpp + CMakeLists.txt
src/lab_02..lab_05/     будущие лабораторные
scripts/                common.py, generate.py, run.py, verify.py, plot.py
data/                   входные матрицы (*.bin в .gitignore)
results/lab_XX/         results.csv, verification.csv, C_n.bin
reports/lab_XX/         графики и summary.csv для отчёта
```

## Задел на следующие лабораторные

- Новая лабораторная = папка `src/lab_XX/` с `main.cpp` и `CMakeLists.txt` — корневой CMake
  подключит её сам. Остальной конвейер (`make run/verify/plot LAB=lab_XX`) не меняется.
- `multiply()` принимает блок строк `rows × n`: OpenMP делит строки между потоками,
  MPI — между процессами; последовательная версия служит эталоном.
- `run.py --prefix "mpirun -np 4"` запускает бинарник через обёртку (MPI, `srun` и т.п.).

## Совместимость с кластером

- C++11, CMake ≥ 3.10, без `-march=native` (архитектура login- и вычислительных узлов может различаться).
- `Makefile` не использует `cmake -S/-B` и пресеты — работает со старым CMake.
  `CMakePresets.json` нужен только для IDE (CMake ≥ 3.20).
- Python-скрипты совместимы с Python 3.6+, нужны только `numpy` и `matplotlib`.
