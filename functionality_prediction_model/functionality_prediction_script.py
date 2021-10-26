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

expert_based_dict = {73.04: ['epoxide','sulfone','sulfoxide', 'amide', 'alcohol', 'aldehyde', 'ether', 'ketone', 'ester', 'carboxylic acid'], #TMB adduct-MeOH
                     59.03: ['epoxide', 'sulfone'], #TMB adduct-Me2O
                     105.07: ['sulfone'], #TMB adduct
                     72.06: ['sulfoxide', 'N,N-disubstituted_hydroxylamine', 'aromatic_tertiary_N-oxide'], #MOP adduct
                     52.04: ['N-oxide_with_nearby_COOH/OH/NH2', 'sulfoxide_with_nearby_COOH/OH/NH2'], #TDMAB adduct-2DMA
                     98.10: ['N-oxide', 'sulfoxide', 'urea', 'pyridine', 'imine']} #TDMAB adduct-DMA
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

"""Selecting Relatives higher than or equal to a predefined cutoff. Defaults has been set to 2.
Then branching ratios are being calculated for the remaining peaks other than the analyte peak"""
def br_calculation(df, analyte, cutoff):
    df_selected = df.loc[df['Relative'] >= relative_cutoff] # select the peaks above a certain relative intensity cutoff
    df_dropped = df_selected.loc[df['m/z'] != analyte] # protonated analyte dropped!
    sum_relative = sum(df_dropped['Relative'])
    df_dropped['Branching_ratios']= (df_dropped['Relative']/sum_relative)*100 #BR calculation
    return df_dropped

def mass_difference(df, analyte):
    df['mass_difference'] = abs(df['m/z'] - analyte)
    return df

def expert_based(df, nr, dictionary):
    funcs = []
    for i in df['mass_difference']:
        for key in dictionary.keys():
            if i >= key-0.6 and i <= key+0.6:
#                print(dictionary[key])
                funcs.append(dictionary[key])
            else:
                continue
            
    return funcs

def ml_based(df, nr, dictionary):
    
    return None



result_df = br_calculation(df, analyte_mz, relative_cutoff)
#print(result_df)

result_df2 = mass_difference(result_df, analyte_mz)

expert_based_funcs = expert_based(result_df2, 'None', expert_based_dict)

print(*expert_based_funcs)


    
