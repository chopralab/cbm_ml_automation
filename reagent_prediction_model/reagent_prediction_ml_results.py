from __future__ import print_function
from rdkit.Chem import *
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
import re
import sys

elemental_composition = "C6H8S2O1"#sys.argv[1]

#elemental_composition = input('Input elemental composition (eg: C6H8N2O0; include Oxygen as zero if not present): ') # user = 'foobar12345'
#rdbe = int(input('RDBE: '))

def create_dictionary(file_nm, list_fp_ids, list_fp_ids_cannot_id, fp_len, reagent):
    listA = []
    listB = []
    dict1 = {}
    for fp_id in list_fp_ids:
        count = 0
        if fp_id in list_fp_ids_cannot_id:
            with open(file_nm) as f:
                for line in f:
            
                    count = count + 1
            
                    x = re.split("\\.", line)
                    m = MolFromSmiles(x[0])
                    
                    for a in range(0,m.GetNumAtoms()):
                        m.GetAtomWithIdx(a).SetFormalCharge(0)
            
                    bi = {}
        
                    bits = AllChem.GetMorganFingerprintAsBitVect(m,fp_len,nBits=2048,bitInfo=bi)
            
                    if (bits[fp_id - 1] == 0):
                        continue
                    
                    listA.append(str(fp_id) + "_" + str(count))
                    dict1[str(fp_id) + "_" + str(count)] = 'not ' + reagent
        else:
            with open(file_nm) as f:
                for line in f:
            
                    count = count + 1
            
                    x = re.split("\\.", line)
                    m = MolFromSmiles(x[0])
                    
                    for a in range(0,m.GetNumAtoms()):
                        m.GetAtomWithIdx(a).SetFormalCharge(0)
            
                    bi = {}
        
                    bits = AllChem.GetMorganFingerprintAsBitVect(m,fp_len,nBits=2048,bitInfo=bi)
            
                    if (bits[fp_id - 1] == 0):
                        continue
                    
                    listB.append(str(fp_id) + "_" + str(count))
                    dict1[str(fp_id) + "_" + str(count)] = reagent
    return dict1


fp_ids = [223, 429, 1172, 470, 1477, 1820, 428, 657] 
fp_ids_cannot_id = [223]

dict_tmb = create_dictionary("training_smiles_tmb.txt", fp_ids, fp_ids_cannot_id, 2, 'TMB')


print(dict_tmb)

N_containing_funcs = ['1172_16', '1172_17', '1172_20', '223_21', '429_15']
S_containing_funcs = ['428_6', '428_7', '428_8', '470_4']
O_containing_funcs = ['223_19', '470_4', '470_5', '657_10', '657_11', '657_12', '657_13', 
                      '1820_12', '1477_1', '1477_2', '1477_3']
O_N_both_containing_funcs = ['223_21']
O_S_both_containing_funcs = ['470_5', '1477_1', '1477_2', '1477_3']


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


elements = find_elements(elemental_composition)
print(elements)

def find_reagents(lst_of_lst):
    elements = lst_of_lst[0]
    numbers = lst_of_lst[1]
  
    if ('S' in elements and numbers[elements.index('S')] >= 1) and ('O' in elements and numbers[elements.index('O')] >= 1):
        reagent = dict_tmb[O_S_both_containing_funcs[0]]
        print(reagent, ', O_S_both_containing')    
    
#    elif 'N' in elements and 'O' in elements:
#        reagent = dict_tmb[O_N_both_containing_funcs[0]]
#        print(reagent, ', O_N_both_containing')
#    
#    elif 'S' in elements:
#        reagent = dict_tmb[S_containing_funcs[0]]
#        print(reagent, ', S_containing')
#        
#    elif 'O' in elements:
#        reagent = dict_tmb[O_containing_funcs[0]]
#        print(reagent, ', O_containing')
        
elements_list_of_list = find_elements(elemental_composition)
find_reagents(elements_list_of_list)    
    




### Functionality prediction module
    
func_groups_can_present_with_TMB = {"N_contain": [1153], 
                           "S_contain": [], 
                           "O_contain": [651,1907, 657], 
                           "O_N_contain": [], 
                           "O_S_contain": [1477,208],
                           "C_only": [1029]}

#print(func_groups_can_present_with_TMB["N_contain"])




























