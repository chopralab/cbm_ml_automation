#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 14:03:17 2021

@author: prageeth_wijewardhane
"""

import pandas as pd

df = pd.read_csv("ion-molecule_reaction_data/diphenyl_sulfoxide_mop_nominal.txt", skiprows = 8, sep = "\t")


def dataframe_preprocess(df):
    df.sort_values(by=['Intensity'], ascending = False, inplace = True)
    df_max_scaled = df.copy()
    column = 'Intensity'
    df_max_scaled['Relative'] = df_max_scaled[column] /df_max_scaled[column].abs().max()
    
    return(df_max_scaled)
    
print(dataframe_preprocess(df))