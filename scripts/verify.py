import argparse
import sys

import numpy as np

from common import matrix_path, read_matrix, result_path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("lab")
    p.add_argument("--sizes", type=int, nargs="+", required=True)
    args = p.parse_args()

    ok = True
    for n in args.sizes:
        ref = read_matrix(matrix_path("A", n)) @ read_matrix(matrix_path("B", n))
        match = np.array_equal(read_matrix(result_path(args.lab, n)), ref)
        ok = ok and match
        print("n={:<5} {}".format(n, "OK" if match else "FAIL"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
