#!/bin/bash

# Set environment
source set_env.sh

# Get bacteria counter data
./process_bacteria.sh

# List of all UKLI data runs
python listRuns.py > listOfRuns.py

# Process last 7 days of data
./submit.sh last_period.txt
# Wait until data is processed.
#qsub -hold_jid "ukli*" -cwd echo 'Done!'
sleep 10m # waiting for something more clever...

# Analyze all data
# - Position analysis
root -b -q  histofit_asym_gauss_std.cc && root -b -q histofit_noise.cc
# - Angular analysis
#root -b -q histofit_asym_cos.cc

# Make root files with results
# - Position analysis
python B1Z_evolution.py && python B1X_evolution.py && python B1noise_evolution.py
# - Angular analysis
#python B1cos_evolution.py

# Finally, let's plot it! SK steering meeting plots
# - Position analysis
root -b -q twoscales_sigma_rel.C
root -b -q twoscales_sigma_rel_3w.C
root -b -q twoscales_spot.C
root -b -q twoscales_const.C
#root -b -q twoscales_dr.C
# - Angular analysis
#root -b -q cos_twoscales_nslope_rel.C
#root -b -q cos_twoscales_sigma_rel.C
