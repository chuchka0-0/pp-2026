import csv
import os
import re
import subprocess

import matplotlib

matplotlib.use("Agg")
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from common import RESULTS, REPORTS, ROOT

BIN = str(ROOT / "src" / "lab_05" / "mandelbrot")
THREADS = [1, 2, 3, 4, 5, 6, 7, 8, 16]
MODES = {"block": "блоки (п. 2)", "interleaved": "чередование строк (п. 4)"}


def run(mode, view, threads, times=False):
    env = dict(os.environ)
    env.pop("BLOCK", None)
    if mode == "block":
        env["BLOCK"] = "1"
    if times:
        env["THREAD_TIMES"] = "1"
    return subprocess.check_output(
        [BIN, "-t", str(threads), "-v", str(view)],
        env=env,
        universal_newlines=True,
        cwd=str(ROOT / "src" / "lab_05"),
    )


def main():
    out = RESULTS / "lab_05"
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for mode in MODES:
        for view in (1, 2):
            for t in THREADS:
                s = float(
                    re.search(r"\(([\d.]+)x speedup", run(mode, view, t)).group(1)
                )
                rows.append([mode, view, t, s])
                print(mode, view, t, s)
    with open(str(out / "results.csv"), "w") as f:
        csv.writer(f, lineterminator="\n").writerows(
            [["mode", "view", "threads", "speedup"]] + rows
        )

    with open(str(out / "thread_times.txt"), "w") as f:
        for t in (2, 3, 4, 8):
            lines = [
                l
                for l in run("block", 1, t, times=True).splitlines()
                if l.startswith("thread")
            ]
            f.write("threads={}\n{}\n".format(t, "\n".join(sorted(lines[-t:]))))

    fig, ax = plt.subplots()
    colors = iter(cm.Purples([0.45, 0.6, 0.8, 0.95]))
    for mode, name in MODES.items():
        for view in (1, 2):
            pts = [(t, s) for m, v, t, s in rows if m == mode and v == view]
            ax.plot(
                *zip(*pts),
                "o-",
                color=next(colors),
                label="{}, view {}".format(name, view)
            )
    ax.plot(THREADS, THREADS, "--", color="gray", label="идеал")
    ax.set_xlabel("Потоки")
    ax.set_ylabel("Ускорение относительно serial")
    ax.grid(True, alpha=0.3)
    ax.legend()
    figures = REPORTS / "lab_05" / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(str(figures / "speedup.png"), dpi=150)
    print("done")


if __name__ == "__main__":
    main()
