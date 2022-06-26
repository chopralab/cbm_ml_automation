#!/bin/bash -i

python Plotting_and_Processing/contour_single.py -x Data/MOP/iteration_5 -y Data/MOP/MOP_chain_5.csv
python Plotting_and_Processing/contour_single.py -x Data/TMB/iteration_5 -y Data/TMB/TMB_chain_5.csv
python Plotting_and_Processing/contour_single.py -x Data/TDMAB/iteration_2 -y Data/TDMAB/TDMAB_chain_2.csv
