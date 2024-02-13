#!/bin/sh

python3 plot-pretest.py 'pretest-ingenieure'
python3 plot-pretest.py 'pretest-sachunterricht'
python3 plot-pretest-vgl-SU-ING.py
python3 plot-posttest.py 'posttest-sachunterricht'
