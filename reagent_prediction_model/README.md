# Reagent Prediction (Prototype)

This repo contains small prototype scripts and data to **predict neutral reagent(s)** for ion–molecule reactions from a molecule’s **elemental composition** and **RDBE** (rings + double-bond equivalents). It also includes utilities to visualize RDKit **Morgan fingerprint bits** as fragment SVGs.

## What's here

- **`neutral_reagent_selection_prototypical.py`** — Rule- and ML-inspired heuristics to suggest **TMB**, **TDMAB**, or **MOP** given an elemental composition string (e.g., `C7H9O2S1`) and an `rdbe` value. Prints expert and ML-based predictions.  
- **`neutral_reagent_selection_prototypical_mono.py`** — A “mono” variant that returns lists from expert and ML rules, computes their intersection/symmetric difference, and prints a **ranked list** (intersection first).  
- **`reagent_prediction_expert_based.py`** — Interactive expert-based recommender: prompts for elemental composition (`C#H#O#N#S#…`) and `RDBE`, then prints a broader set of suggested reagents (e.g., DEMB, TMB, TDMAB, DEADMB, MOP, etc.).  
- **`reagent_prediction_ml_results.py`** — Fingerprint‑bit–driven prototype that builds a dictionary of **TMB-associated fragments** from training SMILES and maps elemental compositions to reagent suggestions; also includes a draft “functionality prediction” section keyed by Morgan bit IDs.  
- **`make_fp_svg_custom.py`** — Given a SMILES file, enumerates present **Morgan bit IDs**, then draws **per‑bit fragment SVGs** for each molecule, saved under `all_dt_identified_mop_fragments/`.  
- **Data**  
  - `training_smiles_tmb.txt` — Reaction transforms / examples used to associate Morgan bits with **TMB**.  
  - `training_smiles_mop.txt` — Small molecules with scores/energies, used in **MOP** prototyping.  
  - `first36.smi` — Example SMILES input for fingerprint visualization.

> **Note:** These scripts are exploratory prototypes with hard‑coded example inputs and paths. Adapt as needed for your datasets and workflows.

## Quick start

### 1)Run the expert + ML heuristic selector
Edit the top of the script to set:
```python
elemental_composition = "C7H9O2S1"
rdbe = 6  # float or int
```
Then run:
```bash
python neutral_reagent_selection_prototypical.py
```
It prints **expert-based** and **ML-based** predictions (TMB / TDMAB / MOP).

**Mono variant with ranking:**
```bash
python neutral_reagent_selection_prototypical_mono.py
```
It returns the expert list, ML list, their **intersection** and **symmetric difference**, and a **ranked** reagent list (intersection first).

### 2) Run the expert-only interactive recommender
```bash
python reagent_prediction_expert_based.py
```
You’ll be prompted for `elemental_composition` (e.g., `C6H8N2O0`) and `RDBE`. It prints one or more expert‑suggested reagents.

### 3) Fingerprint‑bit prototypes (TMB mapping)
- Confirm paths at the top of `reagent_prediction_ml_results.py` (uses `training_smiles_tmb.txt`).
- Run:
```bash
python reagent_prediction_ml_results.py
```
This builds a dictionary of **Morgan bit → reagent** associations from training rules and can map elemental patterns to a suggested reagent.

### 4) Draw fragment SVGs for Morgan bits
- Put your SMILES into `first36.smi` (or update `file_nm` in the script).
- Run:
```bash
python make_fp_svg_custom.py
```
The script identifies present bit IDs across molecules, then for each bit & molecule draws an **SVG** into `all_dt_identified_mop_fragments/`.

## Inputs & Outputs (at a glance)

- **Inputs**: `elemental_composition` like `C12H11O1S1` and an `rdbe` value; optional SMILES files for FP visualization.
- **Outputs**: Printed reagent suggestions (expert/ML), and **SVG fragment visualizations** for selected Morgan bits.

## Caveats / Notes
- Thresholds, bit IDs, and file paths are **hard-coded** in places; adjust for your data.
- Prototype heuristics are intended as **starting points**; validate against held‑out experiments before production use.
- Scripts reset formal charges to zero before fingerprinting to stabilize bit extraction.

## Suggested next steps
- Move constants and thresholds to a **config file** (YAML/JSON).
- Wrap selectors into a **CLI** with `argparse`.
- Add **unit tests** against known examples and negative controls.
- Package as a module and expose a simple Python API (e.g., `predict_reagent(composition, rdbe)`).

---
