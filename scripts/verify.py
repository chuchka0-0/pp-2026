"""
Верификация: сравнение results/<lab>/C_<n>.bin с эталоном numpy A @ B.
"""

import argparse
import csv
import sys

import numpy as np

from common import RESULTS, input_path, output_path, read_matrix

TOLERANCE = 1e-10  # допустимая относительная погрешность max|C - ref| / max|ref|


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("lab")
    p.add_argument("--sizes", type=int, nargs="+", required=True)
    args = p.parse_args()

    rows, all_ok = [], True
    for n in args.sizes:
        ref = read_matrix(input_path("A", n)) @ read_matrix(input_path("B", n))
        err = float(
            np.abs(read_matrix(output_path(args.lab, n)) - ref).max()
            / np.abs(ref).max()
        )
        ok = err < TOLERANCE
        all_ok = all_ok and ok
        rows.append([n, "{:.3e}".format(err), "OK" if ok else "FAIL"])
        print("n={:<5} rel_err={:.3e} {}".format(n, err, rows[-1][2]))

    with open(str(RESULTS / args.lab / "verification.csv"), "w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["n", "rel_err", "status"])
        writer.writerows(rows)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
