import argparse

import numpy as np

from common import DATA, matrix_path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sizes", type=int, nargs="+", required=True)
    p.add_argument("--seed", type=int, default=1)
    args = p.parse_args()

    DATA.mkdir(exist_ok=True)
    for n in args.sizes:
        rng = np.random.RandomState(args.seed + n)
        for name in ("A", "B"):
            m = rng.randint(0, 10, (n, n))
            np.savetxt(
                str(matrix_path(name, n)), m, fmt="%d", header=str(n), comments=""
            )
        print("n={}".format(n))


if __name__ == "__main__":
    main()
