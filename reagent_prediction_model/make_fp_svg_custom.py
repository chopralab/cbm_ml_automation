from __future__ import print_function
from rdkit.Chem import *
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
import re

file_nm = "first36.smi" #sys.argv[1]
fp_len = 1 #int(sys.argv[2])
fps = []

count = 0
with open(file_nm) as f:
    for line in f:

        count = count + 1

        x = re.split("\\.", line)
        m = MolFromSmiles(x[0])
#            print(x[0])
        
        for a in range(0,m.GetNumAtoms()):
            m.GetAtomWithIdx(a).SetFormalCharge(0)

        bi = {}
        bits = AllChem.GetMorganFingerprintAsBitVect(m,fp_len,nBits=2048,bitInfo=bi)
#        print(bi.keys())  
        
        for key in bi.keys():
            if key not in fps:
                fps.append(key)
            else:
                continue


#print(bi.keys())
print(fps)

for fp_id in fps:
    count = 0
    count2 = 0
    with open(file_nm) as f:
        for line in f:
    
            count = count + 1
    
            x = re.split("\\.", line)
            m = MolFromSmiles(x[0])
#            print(x[0])
            
            for a in range(0,m.GetNumAtoms()):
                m.GetAtomWithIdx(a).SetFormalCharge(0)
    
            bi = {}
            bits = AllChem.GetMorganFingerprintAsBitVect(m,fp_len,nBits=2048,bitInfo=bi)
    
    
            if (bits[fp_id - 1] == 0):
                count2 = count2+1
                continue
    
            print(bi[fp_id - 1])
    
            mfp3_svg = Draw.DrawMorganBit(m, fp_id - 1, bi)
    
            out = open("all_dt_identified_mop_fragments/%d_%d.svg" % (fp_id, count), 'w')
            out.write(mfp3_svg)
            out.close()
    print(count2)

#print(bi.keys())



