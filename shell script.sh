#!/usr/bin/env bash

python dfr_simulation.py -M uniform -P 0.1 --fec --trace
python dfr_simulation.py -M sgm -P 0.1 --fec --trace