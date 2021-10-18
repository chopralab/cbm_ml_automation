from __future__ import print_function

#elemental_composition = 'C4H7O2N1' #sys.argv[1]
elemental_composition = input('Input elemental composition (eg: C6H8N2O0; include Oxygen as zero if not present): ') # user = 'foobar12345'
rdbe = int(input('RDBE: '))

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
    

def find_reagents(lst_of_lst):
    elements = lst_of_lst[0]
    numbers = lst_of_lst[1]
    
    reagents = ['DEMB', 'DEMB + CD3OD', 'TMB', 'TDMAB', 'DEADMB', 'MOP', 'DEE', 'Ethyl vinyl ether',
                'TMMS', 'DMA', 'TMP', 'HMPA', 'DEMP', 'DMDS']
    if 'S' not in elements:
        if ('O' in elements and numbers[elements.index('O')] >= 1) or ('O' in elements and numbers[elements.index('O')] >= 1 and 'N' in elements and rdbe >= 0.5) or ('O' in elements and numbers[elements.index('O')] >= 2):
            reagent = reagents[0]
            print('\n', reagent)
            
    if 'S' not in elements:
        if ('O' in elements and numbers[elements.index('O')] >= 1) or ('O' in elements and 'N' in elements and rdbe >= 0.5 and numbers[elements.index('O')] >= 1):
            reagent = reagents[1]
            print('\n',reagent)

    if ('S' in elements and 'O' in elements and numbers[elements.index('O')] >= 2) or ('O' in elements and 'N' in elements and rdbe >= 0.5 and numbers[elements.index('O')] >= 1) or ('O' in elements and rdbe >= 0.5 and numbers[elements.index('O')] >= 1) or  ('O' in elements and numbers[elements.index('O')] >= 2):
        reagent = reagents[2]
        print('\n',reagent)

    if ('S' in elements and 'O' in elements and numbers[elements.index('O')] >= 1 and rdbe >= 0.5) or ('O' in elements and numbers[elements.index('O')] >= 1 and 'N' in elements and rdbe >= 0.5):
        reagent = reagents[3]
        print('\n',reagent)
    
    if 'S' not in elements:
        if ('O' in elements and numbers[elements.index('O')] >= 1 and 'N' in elements and rdbe >= 0.5):
            reagent = reagents[4]
            print('\n',reagent)
            
    if ('S' in elements and 'O' in elements and numbers[elements.index('O')] >= 1 and rdbe >= 0.5) or ('O' in elements and numbers[elements.index('O')] >= 1 and 'N' in elements) or ('N' in elements and numbers[elements.index('N')] >= 2):
        reagent = reagents[5]
        print('\n',reagent)
     
    if 'S' not in elements:
        if ('N' in elements and numbers[elements.index('N')] >= 2) or ('N' in elements and numbers[elements.index('O')] >= 2 and rdbe >= 0.5):
            reagent = reagents[6]
            print('\n',reagent)
    
    if 'S' not in elements:
        if ('O' in elements and numbers[elements.index('O')] >= 2) and rdbe >= 0.5:
            reagent = reagents[7]
            print('\n',reagent)
    
    if ('S' in elements and 'O' in elements and numbers[elements.index('O')] >= 2) or ('O' in elements and numbers[elements.index('O')] >= 2) or ('N' in elements and 'O' in elements and numbers[elements.index('O')] >= 2):
        reagent = reagents[8]
        print('\n',reagent)
        
    if ('N' in elements and 'O' in elements and numbers[elements.index('O')] >= 1):
       reagent = reagents[9]
       print('\n',reagent) 
        
    if ('S' in elements and 'O' in elements and (numbers[elements.index('O')] >= 2)):
       reagent = reagents[10]
       print('\n',reagent) 
       
    if 'N' in elements:
        reagent = reagents[11]
        print('\n',reagent)
        
    if 'N' in elements:
        reagent = reagents[12]
        print('\n',reagent)
        
    if 'N' in elements and 'O' in elements and numbers[elements.index('O')] >= 1:
        reagent = reagents[13]
        print('\n',reagent)
    
       
elements_list_of_list = find_elements(elemental_composition)
find_reagents(elements_list_of_list)





























