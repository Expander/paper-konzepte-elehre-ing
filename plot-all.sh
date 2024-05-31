#!/bin/sh

python3 plot-pretest.py 'pretest-ingenieure-all'
python3 plot-pretest.py 'pretest-ingenieure-matched'
python3 plot-pretest.py 'pretest-sachunterricht'
python3 plot-pretest-vgl-SU-ING.py
python3 plot-posttest.py 'posttest-sachunterricht'
python3 plot-posttest.py 'posttest-ingenieure'
