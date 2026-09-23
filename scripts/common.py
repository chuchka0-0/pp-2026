"""
Общие пути и ввод-вывод матриц (тот же формат, что в src/common/matrix.hpp).
"""

from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
REPORTS = ROOT / "reports"
FIELDS = ["lab", "n", "workers", "time_s", "ops", "gflops"]


def input_path(name, n):
    return DATA / "{}_{}.bin".format(name, n)


def output_path(lab, n):
    return RESULTS / lab / "C_{}.bin".format(n)


def read_matrix(path):
    with open(str(path), "rb") as f:
        n = int(np.fromfile(f, "<i8", 1)[0])
        return np.fromfile(f, "<f8", n * n).reshape(n, n)


def write_matrix(path, m):
    with open(str(path), "wb") as f:
        np.array([m.shape[0]], "<i8").tofile(f)
        np.ascontiguousarray(m, "<f8").tofile(f)
