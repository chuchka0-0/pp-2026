import argparse
import itertools
import os
import shlex
import subprocess

from common import ROOT, RESULTS, matrix_path, result_path


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("lab")
    p.add_argument("--sizes", type=int, nargs="+", required=True)
    p.add_argument("--workers", type=int, nargs="+", default=[1])
    p.add_argument("--repeats", type=int, default=3)
    p.add_argument("--prefix", default="")
    args = p.parse_args()

    binary = str(ROOT / "build" / "src" / args.lab / args.lab)
    out = RESULTS / args.lab
    out.mkdir(parents=True, exist_ok=True)
    table = out / "results.csv"
    if not table.exists():
        table.write_text("lab,n,workers,time_s,ops,gops\n")

    with open(str(table), "a") as f:
        for n, w in itertools.product(args.sizes, args.workers):
            env = dict(os.environ, OMP_NUM_THREADS=str(w))
            cmd = shlex.split(args.prefix.format(w=w)) + [
                binary,
                str(matrix_path("A", n)),
                str(matrix_path("B", n)),
                str(result_path(args.lab, n)),
            ]
            for _ in range(args.repeats):
                line = subprocess.check_output(
                    cmd, env=env, universal_newlines=True
                ).strip()
                f.write(line + "\n")
                f.flush()
                print(line)


if __name__ == "__main__":
    main()
