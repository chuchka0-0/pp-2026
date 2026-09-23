-include .env

LAB ?= lab_01
SIZES ?= 200 400 800 1200 1600 2000
SEED ?= 42
REPEATS ?= 3
PYTHON ?= python3
BUILD ?= build

.PHONY: all build data run verify plot clean clean-results

all: build data run verify plot

build:
	mkdir -p $(BUILD) && cd $(BUILD) && cmake .. -DCMAKE_BUILD_TYPE=Release && $(MAKE)

data:
	$(PYTHON) scripts/generate.py --seed $(SEED) --sizes $(SIZES)

run:
	$(PYTHON) scripts/run.py $(LAB) --sizes $(SIZES) --repeats $(REPEATS)

verify:
	$(PYTHON) scripts/verify.py $(LAB) --sizes $(SIZES)

plot:
	$(PYTHON) scripts/plot.py reports/$(LAB) $(wildcard results/*/results.csv)

clean:
	rm -rf $(BUILD)

clean-results:
	rm -f results/$(LAB)/*.csv results/$(LAB)/*.bin
