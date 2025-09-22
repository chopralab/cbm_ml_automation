# Interpretable Machine Learning-based Automated HPLC/MS<sup>2</sup> Platform

To automate ion–molecule reactions in a mass spectrometer, we have intoduced multiple modules for various workflows needed for human-in-the-loop experimentation.

# Getting Started

A Conda enviornment is provided for reagent selection and ion–molecule reaction interpretation modules (`enviornment.yml`).

This can be installed using the command:
```
> conda env create -f environment.yml
```

A seperate list of requirements are described in the `Paddy_PUMP` directory, in addition to a brief workflow description.

# Replicating Workflows

Each module has instructions in their respective directories:

- decision_tree_models
- functionality_prediction_model
- reagent_prediction_model
- Paddy_PUMP