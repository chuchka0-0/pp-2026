from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
REPORTS = ROOT / "reports"


def matrix_path(name, n):
    return DATA / "{}_{}.txt".format(name, n)


def result_path(lab, n):
    return RESULTS / lab / "C_{}.txt".format(n)


def read_matrix(path):
    with open(str(path)) as f:
        n = int(f.readline())
        return np.array(f.read().split(), dtype=np.int64).reshape(n, n)
