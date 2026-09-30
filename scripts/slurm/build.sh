#!/bin/bash
set -euo pipefail

MPICXX="${MPICXX:-mpicxx}"
if ! command -v "$MPICXX" >/dev/null 2>&1; then
    command -v mpiicpc >/dev/null 2>&1 && MPICXX=mpiicpc || {
    echo "ОШИБКА: не найден mpicxx/mpiicpc. Сначала: module load intel/mpi5" >&2; exit 1; }
fi

echo "Компилятор: $MPICXX"
"$MPICXX" -std=c++11 -O3 -I src src/lab_03/main.cpp -o lab_03
echo "Готово: ./lab_03"
