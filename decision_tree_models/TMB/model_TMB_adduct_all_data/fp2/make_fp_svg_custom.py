from __future__ import print_function
from rdkit.Chem import *
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
import re
import sys

file_nm = sys.argv[1]
fp_len = int(sys.argv[2])
fp_id = int(sys.argv[3])

count = 0

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

        print(bi[fp_id - 1])

        mfp3_svg = Draw.DrawMorganBit(m, fp_id - 1, bi)

        out = open("%d_%d.svg" % (fp_id, count), 'w')
        out.write(mfp3_svg)
        out.close()
