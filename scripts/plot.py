import argparse
import csv
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np

from common import RESULTS, REPORTS

XLABEL = {"lab_02": "Потоки", "lab_03": "Процессы", "lab_04": "Размер блока"}


def purples(count):
    return [cm.Purples(x) for x in np.linspace(0.45, 0.95, max(count, 1))]


def load(lab):
    data = defaultdict(lambda: defaultdict(list))
    for name in ("lab_01", lab):
        csv_file = RESULTS / name / "results.csv"
        if not csv_file.exists():
            continue
        with open(str(csv_file)) as f:
            for r in csv.DictReader(f):
                data[(name, int(r["workers"]))][int(r["n"])].append(float(r["time_s"]))
    return {
        key: {n: float(np.median(v)) for n, v in by_n.items()}
        for key, by_n in data.items()
    }


def save(fig, path):
    fig.tight_layout()
    fig.savefig(str(path), dpi=150)
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("lab")
    args = p.parse_args()
    lab = args.lab
    figures = REPORTS / lab / "figures"
    figures.mkdir(parents=True, exist_ok=True)

    series = load(lab)

    items = sorted(series.items())
    colors = purples(len(items))
    fig, ax = plt.subplots()
    for ((name, w), by_n), color in zip(items, colors):
        ns = sorted(by_n)
        label = (
            name if name == "lab_01" else "{}={}".format(XLABEL.get(lab, "workers"), w)
        )
        ax.plot(ns, [by_n[n] for n in ns], "o-", color=color, label=label)
    ax.set_xlabel("Размер матрицы n")
    ax.set_ylabel("Время, с")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    ax.legend()
    save(fig, figures / "time_by_size.png")

    base = series.get(("lab_01", 1))
    own = sorted((w, by_n) for (name, w), by_n in series.items() if name == lab)
    if base and own:
        big = max(base)
        fig, ax = plt.subplots()
        ws = [w for w, by_n in own if big in by_n]
        s = [base[big] / dict(own)[w][big] for w in ws]
        ax.plot(ws, s, "o-", color=cm.Purples(0.85), label="S на n={}".format(big))
        if lab != "lab_04":
            ax.plot(ws, ws, "--", color="gray", label="идеал")
        ax.set_xlabel(XLABEL.get(lab, "workers"))
        ax.set_ylabel("Ускорение S")
        ax.grid(True, alpha=0.3)
        ax.legend()
        save(fig, figures / "speedup.png")

    print("figures saved to {}".format(figures))


if __name__ == "__main__":
    main()
