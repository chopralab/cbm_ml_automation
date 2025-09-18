# Paddy-PUMP
<div align = "center">
  <img src="https://github.com/chopralab/cbm_ml_automation/blob/main/Paddy_PUMP/GUI/Paddy_PUMP.png">
</div>

All software needed to run Paddy-PUMP can be found in the `GUI` directory.  The app is run with python from the `GUI` directory simply with:
```
python GUI_Main.py
```
# Usage
To simulate usage of Paddy-PUMP, one should first select a channel and then click the 'Recover Pump-Pulse' button.  From there, the user will be prompted to select a Paddy pickle file, which can be found in the `Data` subdirectories (i.e. `Data/MOP/iteration_0.pickle`).  One should then click 'Process MS Data' and then select the associated csv file (i.e. `Data/MOP/iteration_0.csv`).
   
# Requirements
The following packages should be installed to use Paddy-PUMP:

- NumPy
- pandas
- SciPy
- Scikit-learn
- PIL

Note that Paddy source code is provided for static importing, and users may need to be mindfull if they have newer versions of Paddy installed via pip.



