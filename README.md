# Interpretable Machine Learning-based Automated HPLC/MS<sup>2</sup> Platform

To automate ion–molecule reactions in a mass spectrometer, we have intoduced multiple modules for various workflows needed for human-in-the-loop experimentation.

# Getting Started

## Julia Setup for Decision Tree Models

The decision-tree models for TMB and TDMAB are implemented in Julia.  
To reproduce the decision-tree training, bootstrapping, and prediction scripts, follow the steps below.

### 1. Install Julia
Please follow instructions at
https://julialang.org/downloads/

### 2. Launch Julia in the working directory

```
Julia
```

```
import Pkg

# Install required packages
Pkg.add(name="DecisionTree", version="0.10.10")
Pkg.add(["CSV", "DataFrames", "Random"])
```

A Conda enviornment is provided for reagent selection and ion–molecule reaction interpretation modules (`enviornment.yml`).

This can be installed using the command:
```
> conda env create -f environment.yml -n cbm_env
```

A new Conda enviornment is provided for with removing system-specific dependencies (`enviornment2.yml`).
This can be installed using the command:
```
> conda env create -f environment2.yml -n cbm_env2
```

If using this envrionment leads to an error. Please do the following:
```
> conda remove pillow
> conda install -c conda-forge "pillow>=9.4" "libtiff>=4.5,<5"
```

A seperate list of requirements are described in the `Paddy_PUMP` directory, in addition to a brief workflow description.

# Replicating Workflows

Each module has instructions in their respective directories:

- decision_tree_models
- functionality_prediction_model
- reagent_prediction_model
- Paddy_PUMP