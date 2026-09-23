# Лабораторные работы по параллельному программированию

Тема: Умножение квадратных матриц.

- C++: последовательная версия, OpenMP, MPI (суперкомпьютер «Сергей Королёв»), CUDA.
- Python: генерация данных, проверка результатов и построение графиков.

| Лабораторная | Тема                       | Исходники                | Отчёт                                      | Результаты                       |
| ------------ | -------------------------- | ------------------------ | ------------------------------------------ | -------------------------------- |
| lab_01       | Последовательное умножение | [src/lab_01](src/lab_01) | [reports/lab_01](reports/lab_01/README.md) | [results/lab_01](results/lab_01) |
| lab_02       | —                          | —                        | —                                          | —                                |
| lab_03       | —                          | —                        | —                                          | —                                |
| lab_04       | —                          | —                        | —                                          | —                                |
| lab_05       | —                          | —                        | —                                          | —                                |

# Подготовка к работе и быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate.bat     # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

# Структура репозитория

```bash
pp-2026/
├── CMakeLists.txt
├── CMakePresets.json
├── Makefile
├── requirements.txt
├── src/
│   ├── CMakeLists.txt
|   └──lab_0X.cpp
├── scripts/
│   ├── common.py
│   ├── plot.py
│   ├── run.py
│   ├── verify.py
│   └── generate.py
├── results/lab_0X/
└── reports/lab_0X/
```