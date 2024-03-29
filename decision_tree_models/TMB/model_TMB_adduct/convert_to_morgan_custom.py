#!/usr/bin/env python

from __future__ import print_function
from rdkit.Chem import *
from rdkit.Chem import AllChem
import re
import sys

file_name = sys.argv[1]
fp_length = int(sys.argv[2])

print("fingerprint,label")

with open(file_name) as f:
    for line in f:
        x = re.split("\\.", line)
#        print(x[0])
        m = MolFromSmiles(x[0])
#        print(m)
        my_invars = []
        for a in range(0,m.GetNumAtoms()):
            m.GetAtomWithIdx(a).SetFormalCharge(0)

        bits = AllChem.GetMorganFingerprintAsBitVect(m,fp_length,nBits=2048)

        y = re.split("\\s+", line.strip())
        print("%s,%s" % (bits.ToBase64(),y[1]))
