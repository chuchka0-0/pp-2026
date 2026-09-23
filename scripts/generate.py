"""
Генерация входных матриц data/A_<n>.bin и data/B_<n>.bin с фиксированным семенем.
"""

import argparse

import numpy as np

from common import DATA, input_path, write_matrix


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sizes", type=int, nargs="+", required=True)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    DATA.mkdir(exist_ok=True)
    for n in args.sizes:
        # RandomState: поток чисел заморожен в numpy и не меняется между версиями
        rng = np.random.RandomState([args.seed, n])
        for name in ("A", "B"):
            write_matrix(input_path(name, n), rng.uniform(-1.0, 1.0, (n, n)))
        print("generated n={}".format(n))


if __name__ == "__main__":
    main()
