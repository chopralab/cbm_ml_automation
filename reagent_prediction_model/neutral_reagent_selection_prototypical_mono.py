#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:51:10 2021

@author: prageeth_wijewardhane
"""
from __future__ import print_function

### Three examples cases
## C12H11O1S1, rdbe = 9
## C7H9O2S1, rdbe = 6
## C5H6N1O1, rdbe = 4

"""S containing"""
## C6H18O2S1, rdbe = 2
## C4H8O2S1, rdbe = 3

"""Epoxides"""
## C4H6O1, rdbe = 2

"""Amines"""
## C6H15N1O0, rdbe = 0
## C6H8N1O0, rdbe = 4

elemental_composition = 'C6H8N1O0' #'C4H7O2N1' #sys.argv[1]
#elemental_composition = input('Input elemental composition (eg: C6H8N2O0; include Oxygen as zero if not present): ') # user = 'foobar12345'
rdbe = 4 # int(input('RDBE: '))

print('Elemental Composition: ',elemental_composition), print('RDBE: ', rdbe)
print('\n')

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
    

def find_reagents_expert(lst_of_lst):
    elements = lst_of_lst[0]
    numbers = lst_of_lst[1]
    
    reagents = ['TMB', 'TDMAB','MOP']

    if ('S' in elements and 'O' in elements and numbers[elements.index('O')] == 2) or ('S' in elements and 'O' in elements and numbers[elements.index('O')] == 2) or ('O' in elements and 'N' in elements and rdbe >= 0.5 and numbers[elements.index('O')] == 1 and numbers[elements.index('N')] == 1) or ('O' in elements and rdbe >= 0.5 and numbers[elements.index('O')] == 1) or  ('O' in elements and numbers[elements.index('O')] == 2):
        reagent = reagents[0]
        print('\n',reagent, '\n')

    if ('S' in elements and 'O' in elements and numbers[elements.index('O')] == 1 and rdbe >= 0.5) or ('O' in elements and numbers[elements.index('O')] == 1 and 'N' in elements and numbers[elements.index('N')] >= 0.5 and rdbe >= 0.5):
        reagent = reagents[1]
        print('\n',reagent, '\n')
    

    if ('S' in elements and 'O' in elements and numbers[elements.index('O')] == 1 and rdbe >= 0.5) or ('O' in elements and numbers[elements.index('O')] == 1 and 'N' in elements and numbers[elements.index('N')] >= 0.5) or ('N' in elements and numbers[elements.index('N')] == 2):
        reagent = reagents[2]
        print('\n',reagent, '\n')
        
#    else:
#        print('No expert-based predictions', '\n')
  

def find_reagents_ml_based(lst_of_lst):
    elements = lst_of_lst[0]
    numbers = lst_of_lst[1]
    
#    print(elements)
#    print(numbers)
    
    reagents = ['TMB', 'TDMAB','MOP']
  
    if (('S' in elements and numbers[elements.index('S')] == 1) and ('O' in elements and numbers[elements.index('O')] >= 1) and rdbe >= 1.5) or (('N' in elements and numbers[elements.index('N')] == 1) and ('O' in elements and numbers[elements.index('O')] == 1) and rdbe >= 0 and rdbe < 4) or (('O' in elements and numbers[elements.index('O')] >= 1) and rdbe >= 2 and rdbe < 4):
        reagent = reagents[0]
        print('\n',reagent, '\n')  
        
    if ('O' in elements and numbers[elements.index('O')] == 1 and rdbe < 0.5) or (('O' in elements and numbers[elements.index('O')] == 1 ) and rdbe >= 0.5 and ('N' in elements and numbers[elements.index('N')] == 0)) or (('O' in elements and numbers[elements.index('O')] == 1) and ('N' in elements and numbers[elements.index('N')] == 1)) or ('N' in elements and numbers[elements.index('N')] == 0):
        reagent = reagents[1]
        print('\n',reagent, '\n') 
    
    if ('S' in elements and numbers[elements.index('S')] == 1 and rdbe >= 0.5 and 'O' in elements and numbers[elements.index('O')] < 2) or ('N' in elements and numbers[elements.index('N')] == 1 and rdbe >= 0.5 and 'O' in elements and numbers[elements.index('O')] == 1) or ('S' in elements and numbers[elements.index('S')] == 1 and  rdbe == 1) or ('O' in elements and numbers[elements.index('O')] == 1 and 'N' in elements and numbers[elements.index('N')] == 1):
        reagent = reagents[2]
        print('\n',reagent, '\n')
        
    
#    else:
#        print('No ML-based predictions')


elements_list_of_list = find_elements(elemental_composition)

print('expert-based neutral reagent predictions:')
find_reagents_expert(elements_list_of_list)

print('\n')
print('\n')

print( 'ML-based neutral reagent predictions:') 
find_reagents_ml_based(elements_list_of_list)


















