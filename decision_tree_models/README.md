# Decision Tree Models – Minimal README

This repo contains small, reproducible pipelines (Julia + optional Python helpers) to train decision‑tree–style models on molecular fingerprints and generate reagent **hit / no‑hit** predictions with bootstrap validation.

## Folder layout

```
decision_tree_models/
├─ TDMAB/
│  ├─ adduct-DMA_training_reactions_smiles.txt
│  ├─ adduct-DMA_test_reactions_smiles.txt
│  ├─ adduct-DMA_all_reactions_smiles.txt
│  ├─ model_TDMAB+H+/
│  ├─ model_TDMAB+H+_full_data/
│  ├─ model_TDMAB_adduct-DMA/
│  ├─ model_TDMAB_adduct-DMA_full_data/
│  ├─ model_TDMAB_adduct-2DMA/
│  └─ model_TDMAB_adduct-2DMA_full_data/
└─ TMB/
   ├─ model_TMB_adduct/
   ├─ model_TMB_adduct_all_data/
   ├─ model_TMB_adduct-Me2O/
   ├─ model_TMB_adduct-Me2O_all_data/
   ├─ model_TMB_adduct-MeOH/
   └─ model_TMB_adduct-MeOH_all_data/
```

Each `model_*` folder contains the Julia scripts and (optionally) Python helpers used to prepare data, train/evaluate, and make predictions:

- `decode.jl` – decode base64 + run‑length–compressed fingerprints into `BitVector`s.
- `prepare_data.jl` – read input CSV/TSV, decode the `fingerprint` column, build `train_matrix`, `train_res`, `test_matrix`.
- `bootstrap.jl` – utilities for feature importance, leave‑one‑out CV, and repeated bootstrap predictions across cutoffs.
- `model.jl` – end‑to‑end bootstrap sweep that writes aggregated metrics and selected features.
- `decision_tree.jl` – example: fit a `DecisionTreeClassifier`, print the tree, and run k‑fold CV.
- `make_predictions.jl` – batch prediction entry point from trained artifacts/matrices.
- *(optional)* `convert_to_morgan_custom.py`, `make_fp_svg_custom.py` – RDKit helpers for Morgan FPs and SVGs.

### Data files
- Files like `adduct-*.txt` hold reaction SMILES (train/test/all). When using the Julia pipeline, you’ll typically convert these into a tabular file with columns:
  - `fingerprint` (base64, compressed bitset expected by `decode.jl`), and
  - `yield` (Float64 for train; omitted/NA for test).
- Example monolithic dataset: `all_data.csv` (when present) with the same columns.

## Quick start (per model folder)

1) **Julia environment**
```julia
using Pkg
Pkg.activate(".")
Pkg.add(["DecisionTree", "CSV", "DataFrames", "Random"])
# optional:
Pkg.add(["Flux", "MLBase"])
```

2) **Prepare matrices**
Place/train/test tables with at least `fingerprint` (+ `yield` for train) in the current `model_*` dir, then:
```julia
include("prepare_data.jl")   # builds train_matrix, train_res, test_matrix
```

3) **Bootstrap modeling (cutoff sweep)**
```julia
include("model.jl")
```
**Outputs** (filenames may vary slightly by script):
- `results_no_equal.csv` – aggregated metrics by cutoff (last rows often store max train accuracy, val kappa).
- `set_bits_no_equal.csv` – active feature bit indices for the train set (with labels).
- `set_bits_test_no_equal.csv` – same for the test set.

4) **Single tree / k‑fold CV (optional)**
```julia
include("decision_tree.jl")
```

5) **Batch predictions (optional)**
```julia
include("make_predictions.jl")
```

## Notes & conventions
- **Labeling rule**: `hit` if `yield > cutoff` else `nohit`; the cutoff is swept (e.g., 0.0→1.0) during bootstrap.
- **Validation**: leave‑one‑out summaries + bootstrap aggregates across many runs.
- **Determinism**: seeds are set with `Random.seed!` in training/eval scripts.
- **Python helpers**: if you need to generate fingerprints/visualizations outside Julia:
  ```bash
  conda install -c rdkit rdkit pandas
  python convert_to_morgan_custom.py
  python make_fp_svg_custom.py
  ```

## Typical workflow by reagent family
- **TDMAB** models use the `TDMAB/` inputs (e.g., `adduct-DMA_*`) and corresponding `model_TDMAB_*` folders.
- **TMB** models live under `TMB/` with separate subfolders per adduct/solvent condition (e.g., `adduct-MeOH`, `adduct-Me2O`).

Keep each `model_*` folder self‑contained (scripts + its data) to reproduce results independently.
