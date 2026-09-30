#!/bin/bash
#SBATCH --job-name=lab_03
#SBATCH --partition=batch
#SBATCH --ntasks-per-node=8
#SBATCH --time=04:00:00
#SBATCH --output=lab_03-%j.out
set -u

SIZES="200 400 800 1200 1600 2000"
NPROCS="1 2 4 8"
REPEATS=3

ROOT="$SLURM_SUBMIT_DIR"
OUT="$ROOT/results/lab_03"
mkdir -p "$OUT"

module load intel/mpi5

echo "lab,n,workers,time_s,ops,gops" > "$OUT/results.csv"
for n in $SIZES; do
    for np in $NPROCS; do
        for r in $(seq $REPEATS); do
            echo ">>> n=$n np=$np"
            mpirun -r ssh -np "$np" "$ROOT/lab_03" \
            "$ROOT/data/A_$n.txt" "$ROOT/data/B_$n.txt" "$OUT/C_$n.txt" >> "$OUT/results.csv"
        done
    done
done
echo "Готово. Результаты в $OUT/"
