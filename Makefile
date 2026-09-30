-include .env

LAB     ?= lab_01
SIZES   ?= 200 400 800 1200 1600 2000
WORKERS ?= 1
REPEATS ?= 3
SEED    ?= 1
PREFIX  ?=
PY      ?= python3

.PHONY: all build data run verify plot clean lab_05
all: build data run verify plot

build:
	cmake -B build && cmake --build build -j

data:
	$(PY) scripts/generate.py --sizes $(SIZES) --seed $(SEED)

run:
	$(PY) scripts/run.py $(LAB) --sizes $(SIZES) --workers $(WORKERS) --repeats $(REPEATS) --prefix "$(PREFIX)"

verify:
	$(PY) scripts/verify.py $(LAB) --sizes $(SIZES)

plot:
	$(PY) scripts/plot.py $(LAB)

clean:
	rm -rf build

lab_05:
	$(MAKE) -C src/lab_05
	$(PY) scripts/lab_05.py
