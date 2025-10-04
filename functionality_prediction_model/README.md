# Ion–Molecule Reaction Analyzer — README

## Script
**`functionality_prediction_script_demo.py`**

## Overview
This script reads a TXT/TSV spectrum table, computes **relative intensities**, filters peaks by a **relative cutoff**, calculates **branching ratios** and **mass differences** from a given analyte m/z, and proposes likely **functional groups** via:
- an **expert‑curated** mass‑shift dictionary, and
- an **ML‑based** fragment→functional‑group mapping (optionally displaying fragment images).

The processed peak table and predicted functions print to stdout; ML fragment images open in your OS image viewer.

---

## Requirements
- Python ≥ 3.8  
- Packages: `pandas`, `Pillow`
```bash
pip install pandas pillow
```

---

## Input
A tabular text file with at least:
- **Mass** — m/z values
- **Intensity** — peak intensities

**Default input path**
```
ion-molecule_reaction_data/diphenyl_sulfoxide_mop_nominal.txt
```

---

## Key Parameters (in‑script defaults)
- `analyte_mz` (float): protonated analyte m/z (default: `203`)
- `elem_comp` (str): elemental composition, e.g. `"C12H11O1S1"`
- `relative_cutoff` (float): min relative intensity to keep (default: `0.01`)
- `expert_based_dict`, `ml_based_dict`: choose one of `TMB`, `MOP`, `TDMAB` (and matching `*_ml`)

---

## Usage
```bash
# default file and settings
python functionality_prediction_script_demo.py

# custom file
python functionality_prediction_script_demo.py -i path/to/data.txt

# custom header rows and separator
python functionality_prediction_script_demo.py -i data.csv --skiprows 10 --sep ","
```

**CLI Arguments**
- `-i, --input` — path to input file (default shown above)
- `--skiprows` — number of header rows to skip (default: `8`)
- `--sep` — column separator (default: tab `\t`)

---

## What it does
1. **Load & preprocess**
   - Sort by `Intensity`
   - `Relative = Intensity / max(Intensity)`
   - Rename `Mass → m/z`
2. **Filter peaks**
   - Keep `Relative ≥ relative_cutoff`
   - Drop analyte peak (`m/z == analyte_mz`)
3. **Metrics**
   - `Branching_ratios` (% of remaining total relative intensity)
   - `mass_difference = m/z − analyte_mz`
4. **Suggest functional groups**
   - **Expert**: mass‑shift lookup + elemental sieve
   - **ML**: fragment→function mapping; optionally display fragment images

---

## Output
- Printed table with `m/z`, `Relative`, `Branching_ratios`, `mass_difference`
- Printed list of expert‑based suggested functions
- ML fragment images displayed (if available)

> Save output table:
```bash
python functionality_prediction_script_demo.py -i data.txt > results.txt
```

---

## Notes
- Image display depends on your OS default viewer (`Pillow`).
- Ensure fragment/image folders exist relative to your run dir (e.g., `mop_frags_jpgs/`, `tmb_frags_jpgs/`, `tdmab_frags_jpgs/`).
- Switch reagent dictionaries by setting `expert_based_dict` / `ml_based_dict` to `TMB`/`TDMAB` variants as needed.
