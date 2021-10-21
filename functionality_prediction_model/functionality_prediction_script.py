#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 11:46:16 2021

@author: prageeth_wijewardhane
"""

import pandas as pd

df = pd.read_csv("rt30ms.csv") # reading the csv file
analyte_mz = 101.1 # protonated analyte m/z to the decimal place as reported in the reading csv file
relative_cutoff = 2 # relative cutoff using . default has been set to 2
elem_comp = ""
rdbe = 2

expert_based_dict = {}
ml_based_dict = {}


def split(word):
    return list(word)

def element_lists(partial_string):
    int_list, str_list = [], [] 
    for item in partial_string:
        try:
            item = int(item)  # searching for integers in the string
        except:
            str_list.append(item)
        else:  # if there are integers, will add it to int_list 
            int_list.append(item)
    final = [str_list, int_list]  # can also add it to dictionary d = {string: integer}
    return final

def find_elements(string):
    l = []
    l.append(string.find("O"))
    l.append(string.find("S"))
    l.append(string.find("N"))
    l.append(string.find("F"))
    l.append(string.find("Cl"))
    l.append(string.find("Br"))
    
    list1 = [i for i in l if i != -1]
    x = min(list1)
    hetero_string = string[x:]
    hetero_elements = element_lists(hetero_string)
    return hetero_elements

def br_calculation(df, analyte, cutoff):
    df_selected = df.loc[df['Relative'] >= relative_cutoff]
    df_dropped = df_selected.loc[df['m/z'] != analyte]
    sum_relative = sum(df_dropped['Relative'])
    df_dropped['Branching_ratios']= (df_dropped['Relative']/sum_relative)*100
    return df_dropped

def mass_difference(df, analyte):
    df['mass_difference'] = abs(df['m/z'] - analyte)
    return df

def expert_based(df, nr, dictionary):  
    return None

def ml_based(df, ):
    return None



result_df = br_calculation(df, analyte_mz, relative_cutoff)
#print(result_df)

result_df2 = mass_difference(result_df, analyte_mz)
print(result_df2)