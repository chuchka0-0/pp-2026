"""
Графики времени и производительности по одному или нескольким results.csv.
"""

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def load(paths):
    series = defaultdict(lambda: defaultdict(list))
    for path in paths:
        with open(path) as f:
            for r in csv.DictReader(f):
                series[(r["lab"], int(r["workers"]))][int(r["n"])].append(
                    float(r["time_s"])
                )
    return series


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("out", help="папка для графиков, например reports/lab_01")
    p.add_argument("csv", nargs="+")
    args = p.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    series = load(args.csv)
    fig_t, ax_t = plt.subplots()
    fig_g, ax_g = plt.subplots()
    summary = [["lab", "workers", "n", "median_time_s", "gflops"]]

    for (lab, workers), by_n in sorted(series.items()):
        ns = sorted(by_n)
        t = np.array([np.median(by_n[n]) for n in ns])
        gflops = 2.0 * np.array(ns, float) ** 3 / t * 1e-9
        # label = "{} (workers={})".format(lab, workers)
        ax_t.plot(ns, t, "o-", color="purple")
        ax_g.plot(ns, gflops, "o-", color="pink")
        summary += [
            [lab, workers, n, "{:.6f}".format(ti), "{:.3f}".format(gi)]
            for n, ti, gi in zip(ns, t, gflops)
        ]

    for ax, fig, ylabel, name in (
        (ax_t, fig_t, "Время, с", "time.png"),
        (ax_g, fig_g, "GFLOP/s", "gflops.png"),
    ):
        ax.set_xlabel("Размер матрицы n")
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(str(out / name), dpi=150)

    with open(str(out / "summary.csv"), "w", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(summary)
    print("plots saved to {}".format(out))


if __name__ == "__main__":
    main()
