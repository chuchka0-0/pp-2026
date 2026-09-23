"""
Запуск бинарника лабораторной по списку размеров.
"""

import argparse
import csv
import shlex
import subprocess

from common import FIELDS, RESULTS, ROOT, input_path, output_path


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("lab")
    p.add_argument("--sizes", type=int, nargs="+", required=True)
    p.add_argument("--repeats", type=int, default=3)
    p.add_argument("--bin", help="путь к бинарнику (по умолчанию build/bin/<lab>)")
    p.add_argument(
        "--prefix", default="", help="команда-обёртка, например 'mpirun -np 4'"
    )
    args = p.parse_args()

    binary = args.bin or str(ROOT / "build" / "src" / args.lab / args.lab)
    out_dir = RESULTS / args.lab
    out_dir.mkdir(parents=True, exist_ok=True)
    table = out_dir / "results.csv"
    new_file = not table.exists()

    with open(str(table), "a", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        if new_file:
            writer.writerow(FIELDS)
        for n in args.sizes:
            cmd = shlex.split(args.prefix) + [
                binary,
                str(input_path("A", n)),
                str(input_path("B", n)),
                str(output_path(args.lab, n)),
            ]
            for _ in range(args.repeats):
                line = (
                    subprocess.check_output(cmd, universal_newlines=True)
                    .strip()
                    .splitlines()[-1]
                )
                writer.writerow(line.split(","))
                f.flush()
                print(line)


if __name__ == "__main__":
    main()
