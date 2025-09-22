#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 11:46:16 2021

@author: prageeth_wijewardhane
"""

import pandas as pd
import itertools
from PIL import Image

"""reading csv files"""
df = pd.read_csv("ion-molecule_reaction_data/diphenyl_sulfoxide_mop_nominal.txt", skiprows = 8, sep = "\t") # diphenyl_sulfoxide
#df = pd.read_csv("ion-molecule_reaction_data/diphenyl_sulfoxide_tmb_nominal.txt", skiprows = 8, sep = "\t") # diphenyl_sulfoxide
#df = pd.read_csv("ion-molecule_reaction_data/diphenyl_sulfoxide_tdmab_nominal.txt", skiprows = 8, sep = "\t") # diphenyl_sulfoxide

#df = pd.read_csv("ion-molecule_reaction_data/methyl_phenyl_sulfone_tmb_nominal.txt", skiprows = 8, sep = "\t") # methyl_phenyl_sulfone
#df = pd.read_csv("ion-molecule_reaction_data/methyl_phenyl_sulfone_mop_nominal.txt", skiprows = 8, sep = "\t") # methyl_phenyl_sulfone
#df = pd.read_csv("ion-molecule_reaction_data/methyl_phenyl_sulfone_tdmab_nominal.txt", skiprows = 8, sep = "\t") # methyl_phenyl_sulfone
#
#df = pd.read_csv("ion-molecule_reaction_data/pyridine_n-oxide_tdmab_nominal.txt", skiprows = 8, sep = "\t") # pyridine_n-oxide
#df = pd.read_csv("ion-molecule_reaction_data/pyridine_n-oxide_tmb_nominal.txt", skiprows = 8, sep = "\t") # pyridine_n-oxide
#df = pd.read_csv("ion-molecule_reaction_data/pyridine_n-oxide_mop_nominal.txt", skiprows = 8, sep = "\t") # pyridine_n-oxide

#### VARIABLES

""" protonated analyte m/z to the decimal place as reported in the reading csv file"""
analyte_mz = 203 # diphenyl_sulfoxide
#analyte_mz = 157 # methyl_phenyl_sulfone
#analyte_mz = 96 # pyridine_n-oxide

"""Relative Cutoff"""
relative_cutoff = 0.01 # MOP relative cutoff
#relative_cutoff = 0.001 # TMB relative cutoff
#relative_cutoff = 0.01 # TDMAB relative cutoff

"""elemental compositions"""
elem_comp = "C12H11O1S1"
rdbe = 7.5

#elem_comp = "C7H9O2S1"
#rdbe = 3.5

#elem_comp = "C5H6N1O1"
#rdbe = 3.5


"""Neutral reagent wise expert based dictionaries"""
TMB = {73.04: ['epoxide','sulfone','sulfoxide', 'amide', 'alcohol', 'aldehyde', 'ether', 'ketone', 'ester', 'carboxylic acid'], #TMB adduct-MeOH
                     59.03: ['epoxide', 'sulfone'], #TMB adduct-Me2O
                     105.07: ['sulfone']} #TMB adduct}
                     
MOP = { 72.06: ['sulfoxide', 'N,N-disubstituted_hydroxylamine', 'aromatic_tertiary_N-oxide' ]} #MOP adduct

TDMAB = {52.04: ['N-oxide_with_nearby_COOH/OH/NH2', 'sulfoxide_with_nearby_COOH/OH/NH2'], #TDMAB adduct-2DMA
                     98.10: ['N-oxide', 'sulfoxide', 'urea', 'pyridine', 'imine']} #TDMAB adduct-DMA


"""Neutral reagent wise ML based dictionaries"""

TMB_ml = {73.04: ['tmb_frags_jpgs/1153_15.svg.jpg', 
                  'tmb_frags_jpgs/651_23.svg.jpg', 
                  'tmb_frags_jpgs/651_26.svg.jpg'], #TMB adduct-MeOH
                     59.03: ['tmb_frags_jpgs/1029_19.svg.jpg',
                             'tmb_frags_jpgs/1907_22.svg.jpg',
                             'tmb_frags_jpgs/470_6.svg.jpg',
                             'tmb_frags_jpgs/1477_3.svg.jpg'], #TMB adduct-Me2O
                     105.07: []} #TMB adduct
MOP_ml = {72.06: ['mop_frags_jpgs/1.jpg',
                  'mop_frags_jpgs/4.jpg',
                  'mop_frags_jpgs/5.jpg',
                  'mop_frags_jpgs/6.jpg',
                  'mop_frags_jpgs/9.jpg',
                  'mop_frags_jpgs/11.jpg',] #MOP adduct
          }

TDMAB_ml = {52.04: ['tdmab_frags_jpgs/14_16.svg.jpg'], #TDMAB adduct-2DMA
            98.10: ['tdmab_frags_jpgs/1276_15.svg.jpg',
                    'tdmab_frags_jpgs/808_15.svg.jpg',
                    'tdmab_frags_jpgs/808_30.svg.jpg',
                    'tdmab_frags_jpgs/1153_33.svg.jpg']
        }
                     
                     

expert_funcs_n_elemental_comps = {'sulfoxide': ['S','O'],
                           'N,N-disubstituted_hydroxylamine': ['N','O'], 
                           'aromatic_tertiary_N-oxide': ['N','O'],
                           'epoxide':['O'],
                           'sulfone':['S','O'],
                           'amide':['N','O'], 
                           'alcohol':['O'], 
                           'aldehyde':['O'], 
                           'ether':['O'], 
                           'ketone':['O'], 
                           'ester':['O'], 
                           'carboxylic acid':['O'],
                           'N-oxide_with_nearby_COOH/OH/NH2':['N','O'], 
                           'sulfoxide_with_nearby_COOH/OH/NH2':['S','O'],
                           'N-oxide':['N','O'], 
                           'urea':['N','O'], 
                           'pyridine':['N'], 
                           'imine':['N']}

ml_funcs_n_elemental_comps = {'tmb_frags_jpgs/1153_15.svg.jpg': ['N'],
                              'tmb_frags_jpgs/651_23.svg.jpg': ['S','O'],
                              'tmb_frags_jpgs/651_26.svg.jpg': ['O'],
                              'tmb_frags_jpgs/1029_19.svg.jpg': ['C'],
                              'tmb_frags_jpgs/1907_22.svg.jpg': ['O'],
                              'tmb_frags_jpgs/470_6.svg.jpg': ['S','O'],
                              'tmb_frags_jpgs/1477_3.svg.jpg': ['S','O'],
                              'tdmab_frags_jpgs/14_16.svg.jpg': ['O'],
                              'tdmab_frags_jpgs/1276_15.svg.jpg': ['O'],
                              'tdmab_frags_jpgs/808_15.svg.jpg': [],
                              'tdmab_frags_jpgs/808_30.svg.jpg':['N','O'],
                              'tdmab_frags_jpgs/1153_33.svg.jpg': ['N'],
                              'mop_frags_jpgs/1.jpg': ['S', 'O'],
                              'mop_frags_jpgs/9.jpg': ['S', 'O'],
                              'mop_frags_jpgs/4.jpg': ['N', 'O'],
                              'mop_frags_jpgs/5.jpg': ['N'],
                              'mop_frags_jpgs/6.jpg': ['N', 'O'],
                              'mop_frags_jpgs/11.jpg': ['N', 'O']
                              
        }



"""Neutral reagent used"""
#expert_based_dict = TDMAB # TMB, MOP, TDMAB
#expert_based_dict = TMB # TMB, MOP, TDMAB
expert_based_dict = MOP # TMB, MOP, TDMAB

"""Neutral reagent used"""
#ml_based_dict = TDMAB_ml
#ml_based_dict = TMB_ml
ml_based_dict = MOP_ml

### Main code

def dataframe_preprocess(df):
    df.sort_values(by=['Intensity'], ascending = False, inplace = True)
    df_max_scaled = df.copy()
    column = 'Intensity'
    df_max_scaled['Relative'] = df_max_scaled[column] /df_max_scaled[column].abs().max()
    df_max_scaled = df_max_scaled.rename(columns={"Mass": "m/z"})
    return(df_max_scaled)

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
    df_dropped['Branching_ratios'] = (df_dropped['Relative']/sum_relative)*100 #BR calculation
    return df_dropped

def mass_difference(df, analyte):
    df['mass_difference'] = df['m/z'] - analyte # abs(df['m/z'] - analyte)
    return df

def expert_based(df, nr, dictionary):
    funcs = []
    for i in df['mass_difference']:
        for key in dictionary.keys():
            if i >= key-1.04 and i <= key+1.04:
#                print(dictionary[key])
                funcs.append(dictionary[key])
            else:
                continue
    return funcs

def func_sieve_expert(elements_lst_of_lst, predicted_func_list, func_and_elements_dict):
    lst_of_lst = elements_lst_of_lst
    elements = lst_of_lst[0]
    numbers = lst_of_lst[1]
    prob_funcs = []
    
    for i in predicted_func_list:
        if(set(elements).issubset(set(func_and_elements_dict[i]))) and numbers[elements.index('O')] > 0:
            prob_funcs.append(i) 
        else:
            continue
    prob_funcs = [i for n, i in enumerate(prob_funcs) if i not in prob_funcs[:n]]     
    return prob_funcs

def ml_based(df, nr, dictionary):
    funcs = []
    for i in df['mass_difference']:
        for key in dictionary.keys():
            if i >= key-1.04 and i <= key+1.04:
#                print(dictionary[key])
                funcs.append(dictionary[key])
            else:
                continue
    return funcs

def flattening(list_of_list):
    flat_list = list(itertools.chain(*list_of_list))
    return flat_list
    
def func_sieve_ml(elements_lst_of_lst, predicted_func_list, func_and_elements_dict):
    lst_of_lst = elements_lst_of_lst
    elements = lst_of_lst[0]
    numbers = lst_of_lst[1]
    prob_funcs = []
    
    for i in predicted_func_list:
        if(set(elements).issubset(set(func_and_elements_dict[i]))) and numbers[elements.index('O')] > 0:
            prob_funcs.append(i) 
        else:
            continue
    prob_funcs = [i for n, i in enumerate(prob_funcs) if i not in prob_funcs[:n]]     
    return prob_funcs

def ml_funcs_disp(lst):
    for file in lst:
        im = Image.open(file)
        im.show()

df1 = dataframe_preprocess(df)
#print(df1)
result_df = br_calculation(df1, analyte_mz, relative_cutoff)
#print(result_df)

result_df2 = mass_difference(result_df, analyte_mz)
print(result_df2)

##Elemental composition preprocess
elements_list_of_list = find_elements(elem_comp)


#Expert Based Part
expert_based_funcs = expert_based(result_df2, 'None', expert_based_dict)
expert_based_funcs = flattening(expert_based_funcs)
print(func_sieve_expert(elements_list_of_list,expert_based_funcs, expert_funcs_n_elemental_comps))

#ML Based Part
ml_based_funcs = ml_based(result_df2, 'None', ml_based_dict)
ml_based_funcs = flattening(ml_based_funcs)
#print(ml_based_funcs)
ml_func_list = func_sieve_ml(elements_list_of_list, ml_based_funcs, ml_funcs_n_elemental_comps)
#print(ml_func_list)
ml_funcs_disp(ml_func_list)



###############################################################################################################################





"""Full expert based dictionary"""
#expert_based_dict = {73.04: ['epoxide','sulfone','sulfoxide', 'amide', 'alcohol', 'aldehyde', 'ether', 'ketone', 'ester', 'carboxylic acid'], #TMB adduct-MeOH
#                     59.03: ['epoxide', 'sulfone'], #TMB adduct-Me2O
#                     105.07: ['sulfone'], #TMB adduct
#                     72.06: ['sulfoxide', 'N,N-disubstituted_hydroxylamine', 'aromatic_tertiary_N-oxide'], #MOP adduct
#                     52.04: ['N-oxide_with_nearby_COOH/OH/NH2', 'sulfoxide_with_nearby_COOH/OH/NH2'], #TDMAB adduct-2DMA
#                     98.10: ['N-oxide', 'sulfoxide', 'urea', 'pyridine', 'imine']} #TDMAB adduct-DMA


# there is an additional condition here and it give more generalized results. So commented out and removed the condition below.
    
#def func_sieve_expert(elements_lst_of_lst, predicted_func_list, func_and_elements_dict):
#    lst_of_lst = elements_lst_of_lst
#    elements = lst_of_lst[0]
#    numbers = lst_of_lst[1]
#    prob_funcs = []
#    
#    for i in predicted_func_list:
#        if(set(func_and_elements_dict[i]).issubset(set(elements))) and numbers[elements.index('O')] > 0 or  (set(elements).issubset(set(func_and_elements_dict[i]))) and numbers[elements.index('O')] > 0:
#            prob_funcs.append(i)
#            print(i)
#            print(func_and_elements_dict[i])
#            print(elements)
#            print('done')   
#        else:
#            continue
#    prob_funcs = [i for n, i in enumerate(prob_funcs) if i not in prob_funcs[:n]]     
#    return prob_funcs





















    
