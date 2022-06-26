#!/bin/bash -i

python Plotting_and_Processing/paddy_scrape.py -x Data/MOP/iteration_5 -y Data/MOP/MOP_chain_5.csv
python Plotting_and_Processing/paddy_scrape.py -x Data/MOP/iteration_0 -y Data/MOP/MOP_chain_0.csv -b True
python Plotting_and_Processing/paddy_scrape.py -x Data/MOP/iteration_1 -y Data/MOP/MOP_chain_1.csv -b True
python Plotting_and_Processing/paddy_scrape.py -x Data/MOP/iteration_2 -y Data/MOP/MOP_chain_2.csv -b True
python Plotting_and_Processing/paddy_scrape.py -x Data/MOP/iteration_3 -y Data/MOP/MOP_chain_3.csv -b True
python Plotting_and_Processing/paddy_scrape.py -x Data/MOP/iteration_4 -y Data/MOP/MOP_chain_4.csv -b True
python Plotting_and_Processing/paddy_scrape.py -x Data/MOP/iteration_5 -y Data/MOP/MOP_chain_5.csv -b True

python Plotting_and_Processing/paddy_scrape.py -x Data/TMB/iteration_5 -y Data/TMB/TMB_chain_5.csv
python Plotting_and_Processing/paddy_scrape.py -x Data/TMB/iteration_0 -y Data/TMB/TMB_chain_0.csv -b True
python Plotting_and_Processing/paddy_scrape.py -x Data/TMB/iteration_1 -y Data/TMB/TMB_chain_1.csv -b True
python Plotting_and_Processing/paddy_scrape.py -x Data/TMB/iteration_2 -y Data/TMB/TMB_chain_2.csv -b True
python Plotting_and_Processing/paddy_scrape.py -x Data/TMB/iteration_3 -y Data/TMB/TMB_chain_3.csv -b True
python Plotting_and_Processing/paddy_scrape.py -x Data/TMB/iteration_4 -y Data/TMB/TMB_chain_4.csv -b True
python Plotting_and_Processing/paddy_scrape.py -x Data/TMB/iteration_5 -y Data/TMB/TMB_chain_5.csv -b True

python Plotting_and_Processing/paddy_scrape.py -x Data/TDMAB/iteration_2 -y Data/TDMAB/TDMAB_chain_2.csv
python Plotting_and_Processing/paddy_scrape.py -x Data/TDMAB/iteration_0 -y Data/TDMAB/TDMAB_chain_0.csv -b True
python Plotting_and_Processing/paddy_scrape.py -x Data/TDMAB/iteration_1 -y Data/TDMAB/TDMAB_chain_1.csv -b True
python Plotting_and_Processing/paddy_scrape.py -x Data/TDMAB/iteration_2 -y Data/TDMAB/TDMAB_chain_2.csv -b True

python Plotting_and_Processing/write_csvs.py