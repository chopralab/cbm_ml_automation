#!/usr/bin/env python3

import argparse
from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs
import itertools
import sys


def read_reactant_smiles(input_path):
    """
    Read SMILES before '>>' from each line of the input file.
    Returns a list of SMILES strings.
    """
    smiles_list = []
    with open(input_path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                left_part = line.split(">>", 1)[0]
            except IndexError:
                print(f"Warning: line {line_num} does not contain '>>', skipping.", file=sys.stderr)
                continue
            smiles = left_part.strip()
            if smiles:
                smiles_list.append(smiles)
    return smiles_list


def smiles_to_fingerprints(smiles_list, radius=2, n_bits=2048):
    """
    Convert a list of SMILES strings to RDKit Morgan fingerprints.
    Returns a list of (smiles, fp) tuples, skipping invalid SMILES.
    """
    fps = []
    for s in smiles_list:
        mol = Chem.MolFromSmiles(s)
        if mol is None:
            print(f"Warning: could not parse SMILES '{s}', skipping.", file=sys.stderr)
            continue
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
        fps.append((s, fp))
    return fps


def average_pairwise_tanimoto(fps):
    """
    Compute the average pairwise Tanimoto similarity for a list of fingerprints.
    fps: list of RDKit fingerprint objects (not tuples).
    Returns (avg_similarity, n_pairs).
    """
    if len(fps) < 2:
        return None, 0

    total = 0.0
    count = 0

    for fp1, fp2 in itertools.combinations(fps, 2):
        sim = DataStructs.TanimotoSimilarity(fp1, fp2)
        total += sim
        count += 1

    avg = total / count if count > 0 else None
    return avg, count


def main():
    parser = argparse.ArgumentParser(
        description="Compute average pairwise Tanimoto similarity of reactant SMILES in a file."
    )
    parser.add_argument(
        "input_file",
        help="Path to input text file (lines like 'SMI1>>SMI2\\tvalue')."
    )
    parser.add_argument(
        "--radius",
        type=int,
        default=2,
        help="Morgan fingerprint radius (default: 2)."
    )
    parser.add_argument(
        "--nbits",
        type=int,
        default=2048,
        help="Number of bits for Morgan fingerprint (default: 2048)."
    )

    args = parser.parse_args()

    # 1) Read SMILES before '>>'
    smiles_list = read_reactant_smiles(args.input_file)
    if not smiles_list:
        print("No valid reactant SMILES found in the file.", file=sys.stderr)
        sys.exit(1)

    print(f"Read {len(smiles_list)} reactant SMILES from {args.input_file}.")

    # 2) Convert to fingerprints
    smiles_fps = smiles_to_fingerprints(smiles_list, radius=args.radius, n_bits=args.nbits)
    if len(smiles_fps) < 2:
        print("Need at least 2 valid molecules to compute pairwise similarity.", file=sys.stderr)
        sys.exit(1)

    _, fps_only = zip(*smiles_fps)

    # 3) Compute average pairwise Tanimoto
    avg_sim, n_pairs = average_pairwise_tanimoto(fps_only)

    if avg_sim is None:
        print("Could not compute average similarity.", file=sys.stderr)
    else:
        print(f"Number of molecule pairs: {n_pairs}")
        print(f"Average pairwise Tanimoto similarity: {avg_sim:.4f}")


if __name__ == "__main__":
    main()
