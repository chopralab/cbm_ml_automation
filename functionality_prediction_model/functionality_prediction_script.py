#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 11:46:16 2021

@author: prageeth_wijewardhane
"""

import pandas as pd

df = pd.read_csv("rt30ms.csv") # reading the csv file
analyte = 101.1 # protonated analyte m/z to the decimal place as reported in the reading csv file
relative_cutoff = 2 # relative cutoff using . default has been set to 2

def br_calculation(df, analyte_mz, cutoff):
    df_selected = df.loc[df['Relative'] >= relative_cutoff]
    df_dropped = df_selected.loc[df['m/z'] != analyte]
    sum_relative = sum(df_dropped['Relative'])
    df_dropped['Branching_ratios']= (df_dropped['Relative']/sum_relative)*100
    return df_dropped

result_df = br_calculation(df, analyte, relative_cutoff)
#print(result_df)