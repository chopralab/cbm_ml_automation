import matplotlib.pyplot as plt
import numpy
from optparse import OptionParser
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.signal import peak_widths
from scipy.spatial import distance
from sklearn import preprocessing
from sklearn import mixture
import math
import sys
sys.path.append('GUI/')
import paddy
from paddy.utils import random_propogation, get_top_fitness, get_param_names



pumping_time = paddy.PaddyParameter(param_range=[1,4,.1],param_type='continuous',limits=[1,4], gaussian='default',normalization = True)
pulsing_time = paddy.PaddyParameter(param_range=[0.000070,0.000180,.000010],param_type='continuous',limits=[0.000070,0.000180], gaussian='default',normalization = True)


class space(object):
    def __init__(self):
        self.pump = pumping_time
        self.pulse = pulsing_time

def dummy_eval_function(input):
    print(input[0])
    print(input[1])
    return(-100)

parser = OptionParser()
parser.add_option("-x", dest="path_var")
parser.add_option("-y", dest="crom_path")

opts,args = parser.parse_args()
path_var = opts.path_var
crom_path = opts.crom_path

paddy_itt = int(crom_path.split("_")[-1 ].split(".")[0])

def pumping_times(paddy_itt):
    """Returns pumping times from a first iteration given pickle."""
    replicates = 4 #may want to make replicates a user input in the future (the number of times paddy values are replicated)
    runner = paddy.utils.paddy_recover(path_var)
    pump_list = []
    print(paddy_itt)
    if int(paddy_itt) == 0:
        print('itt is 0')
        for i in range(10):
            pump_list.append(runner.seed_params[i][0][0])
    else:
        for i in np.arange(runner.generation_data[str(paddy_itt)][0],runner.generation_data[str(paddy_itt)][1]):
            print(np.arange(runner.generation_data[str(paddy_itt)][0],runner.generation_data[str(paddy_itt)][1]))
            pump_list.append(runner.seed_params[i][0][0])
    # we will probably want to write the tuning pulses
    times = [1.0,2.0,3.0,4.0,5.0]
    time = 7#time when the initial trial startsw
    print(len(pump_list))
    for i in pump_list:
        for j in range(replicates):
            times.append(round(i+time,1))
            time = time + i
        time = time + 3.0
    return(times,pump_list)



runner = paddy.utils.paddy_recover(path_var)

dft = pd.read_csv(crom_path,skiprows=4)
dft.columns=['Time','Intensity']
dft['Time'] = pd.to_numeric(dft['Time'], errors='coerce')
dft['Intensity'] = pd.to_numeric(dft['Intensity'], errors='coerce')
dft = dft.dropna(subset=['Time'])
dft = dft.dropna(subset=['Intensity'])
#assign dfx (time) as X values, and convert to numpy
dfx = dft['Time'].to_numpy()
dfy = dft['Intensity'].to_numpy()
peak_list = -np.sort(-dfy)
#GMM# 
# Number of samples per component
print(peak_list)

X = []
for i in range(len(peak_list)):
    X.append([i,peak_list[i]])
X = np.array(X)

lowest_bic = np.infty
bic = []
n_components_range = [6]
cv_types = ["full"]
for cv_type in cv_types:
    for n_components in n_components_range:
        # Fit a Gaussian mixture with EM
        gmm = mixture.GaussianMixture(
            n_components=n_components, covariance_type=cv_type
        )
        gmm.fit(X)
        bic.append(gmm.bic(X))

Y_ = gmm.predict(X)

comp_list = []
for i in range(6):
    comp_list.append(max(X[Y_ == i, 1]))

min_comp = np.argmin(comp_list)
####

peaks, _ = find_peaks(dfy, height = (max(X[Y_ == min_comp, 1])*2)+1500, distance = 3.5)
#peak width at 1/2 peak height
results_half = peak_widths(dfy, peaks, rel_height=0.5)

lower = []
higher = []
for i , j in zip(results_half[2], results_half[3]):
    remainders = [i % 1 , j % 1]
    x0_times = [dfx[int(i-remainders[0])] , dfx[int(j-remainders[1])]]
    x1_times = [dfx[int(i-remainders[0]+1)] , dfx[int(j-remainders[1]+1)]]
    lower.append(x0_times[0]+remainders[0]*(x1_times[0]-x0_times[0]))
    higher.append(x0_times[1]+remainders[1]*(x1_times[1]-x0_times[1]))

width_list = np.array([results_half[1],lower,higher])
#plot data
#looks fine if tuning peaks are first
times,pump_list = pumping_times(paddy_itt)
data = {'peaks':peaks, 'result_width': results_half[0] }
#Turn dictionary into pandas dataframe
dft2 = pd.DataFrame.from_dict(data)
peak_res = []
for ind in dft2.index[:-1]:
    resolution = (dft2['peaks'][ind+1]-dft2['peaks'][ind])/(
                    dft2['result_width'][ind]+dft2['result_width'][ind+1])
    resolution = '{:.2f}'.format(resolution)
    peak_res.append(resolution)
    peak_res_panda = pd.DataFrame(peak_res)

time_widths = []
for i, j in zip(lower,higher):
    time_widths.append(j-i) 

data = {'peaks':peaks, 'result_width': time_widths }
#Turn dictionary into pandas dataframe
dft2 = pd.DataFrame.from_dict(data)
peak_res = []
for ind in dft2.index[:-1]:
    resolution = (dfx[dft2['peaks'][ind+1]]-dfx[dft2['peaks'][ind]])/(
                    dft2['result_width'][ind]+dft2['result_width'][ind+1])
    #resolution = '{:.2f}'.format(resolution)
    peak_res.append(resolution)
    peak_res_panda = pd.DataFrame(peak_res)

orient = None
orienting = True
while orienting:#getting the tuning peaks
    for i in range(len(peaks)):
    #this is not fool proof, but should work for most cases thrown
        if (dfx[peaks[i+4]] - dfx[peaks[i]])*60 > 3.5:
            if (dfx[peaks[i+4]] - dfx[peaks[i]])*60 < 4.5:
                if (dfx[peaks[i+5]] - dfx[peaks[i+4]])*60 < (2+pump_list[0] + .5):#bug
                    if (dfx[peaks[i+5]] - dfx[peaks[i+4]])*60 > (2+pump_list[0] - .5):
                        orienting = False
                        orient = i + 4 #this is the last tuning peak
                        break

thresh_vals = [dfx[peaks][orient]*60+(2+pump_list[0])/2]
thresh_vals.append(thresh_vals[0]+(pump_list[0]*3.5+2.5)+pump_list[1]*.5)#the 3.5 is representive of the 4 replicates (was 9.5 whern 10 etc.)
c = 2
for i in pump_list[1:]:
    if c != len(pump_list):
        temp = i * 3.5 + thresh_vals[-1] + 3 + pump_list[c] * .5
    else:
        temp = i * 3.5 + thresh_vals[-1] + 3 + 2
    thresh_vals.append(temp)
    c += 1

times,pump_list = pumping_times(paddy_itt)

fitness_list = []
for i in range(len(thresh_vals)-1):
    fitness_list.append([])
t = 0
for i in peaks[orient+1:]:
    if t < len(thresh_vals)-1:
        if dfx[i]*60 > thresh_vals[1+t]:
            t += 1
    fitness_list[t].append(i)
c = 0
for z in fitness_list:
    if len(z) != 4:
        fitness_list[c] = -9999999
    else:
        results_half = peak_widths(dfy, z, rel_height=0.5)
        lower = []
        higher = []
        for i , j in zip(results_half[2], results_half[3]):
            remainders = [i % 1 , j % 1]
            x0_times = [dfx[int(i-remainders[0])] , dfx[int(j-remainders[1])]]
            x1_times = [dfx[int(i-remainders[0]+1)] , dfx[int(j-remainders[1]+1)]]
            lower.append(x0_times[0]+remainders[0]*(x1_times[0]-x0_times[0]))
            higher.append(x0_times[1]+remainders[1]*(x1_times[1]-x0_times[1]))
        width_list = np.array([results_half[1],lower,higher])
        data = {'peaks':z, 'result_width': results_half[0] }
        #Turn dictionary into pandas dataframe
        dft2 = pd.DataFrame.from_dict(data)
        peak_res = []
        for ind in dft2.index[:-1]:
            resolution = (dft2['peaks'][ind+1]-dft2['peaks'][ind])/(
                        dft2['result_width'][ind]+dft2['result_width'][ind+1])
            peak_res.append(resolution)
        fitness_list[c] = (sum(peak_res)/3)
    c += 1


#This block writes over seed fitness
#curently just maximizes fitness
#sense it iterates off of paddy seed indexi, it can be used with chromatograms containing more peaks than needed (demo use)
if int(paddy_itt) == 0:
    for i in range(10):
        runner.seed_fitness[i] = - ( ( ( fitness_list[i] - 2.5 ) ** 2 ) ** .5 )


if int(paddy_itt) != 0:
    c = 0
    for i in np.arange(runner.generation_data[str(paddy_itt)][0],runner.generation_data[str(paddy_itt)][1]):
        runner.seed_fitness[i] = - ( ( ( fitness_list[c] - 2.5 ) ** 2 ) ** .5 )
        c += 1

res = []
for i in runner.seed_fitness:
    res.append(i)

pumps = []
pulses = []
for i in runner.seed_params:
    pumps.append(round(i[0][0],1))
    pulses.append(round(i[1][0],5))


#####
z_set = set()
z_list = []
for i in zip(pumps,pulses):
    z_set.add(i)

z_dic = {}
for i in z_set:
    z_dic[str(i)] = []

for i,j in zip(zip(pumps,pulses),res):
    z_dic[str(i)].append(j)

x = np.linspace(1,4,31)
x = np.round(x,2)
y = np.linspace(0.000070,0.000180,12)
y = np.round(y,5)
z = np.zeros((31,12))

for i in range(len(z)):
    for j in range(len(z[0])):
        z[i][j] = 0.5

c = 0 
res_vals = []
for i in z_dic.keys():
    k = i.split(', ')
    res_vals.append(( sum(z_dic[i])/len(z_dic[i]) ))# Gaurav eddit post 1:1

i_max = np.max(res_vals)
i_min = np.min(res_vals)

c = 0 
res_vals = []
for i in z_dic.keys():
    k = i.split(', ')
    z[np.where(x==np.float64(k[0][1:]))[0][0]][np.where(y==np.float64(k[1][:-1]))[0][0]] = ((  sum(z_dic[i])/len(z_dic[i]) )  - i_min)/(i_max-i_min)


rgnt = crom_path.split('_')[-3].split('/')[-1]
#plt.contourf(y,x,z2,1000,cmap='RdBu')#needed for TDMAB
plt.contourf(y,x,z,100,cmap='RdBu')#not bad
if rgnt == 'TDMAB':
    plt.plot([pulses[7],pulses[10],pulses[23]],[pumps[7],pumps[10],pumps[23]],linewidth=2.5,c='k')#TDMAB_4_chain2
    plt.plot([pulses[7],pulses[10],pulses[23]],[pumps[7],pumps[10],pumps[23]],linewidth=1.5,c='white')#TDMAB_4_chain2

if rgnt == "TMB":
    plt.plot([pulses[6],pulses[15],pulses[58]],[pumps[6],pumps[15],pumps[58]],linewidth=2.5,c='k')#TMB_1_chain5
    plt.plot([pulses[6],pulses[15],pulses[58]],[pumps[6],pumps[15],pumps[58]],linewidth=1.5,c='white')#TMB_1_chain5

if rgnt == "MOP":    
    plt.plot([pulses[0],pulses[35],pulses[61]],[pumps[0],pumps[35],pumps[61]],linewidth=2.5,c='k')#MOP_2_chain5
    plt.plot([pulses[0],pulses[12],pulses[53]],[pumps[0],pumps[12],pumps[53]],linewidth=2.5,c='k')#MOP_2_chain5
    plt.plot([pulses[0],pulses[35],pulses[61]],[pumps[0],pumps[35],pumps[61]],linewidth=1.5,c='white')#MOP_2_chain5
    plt.plot([pulses[0],pulses[12],pulses[53]],[pumps[0],pumps[12],pumps[53]],linewidth=1.5,c='white')#MOP_2_chain5

cbar = plt.colorbar(ticks=[0,.25,.5,.75,1])
tick_font_size = 16
cbar.ax.tick_params(labelsize=tick_font_size)
plt.xticks(np.arange(0.00008,0.00019,0.00002),['80','100','120','140','160','180'],fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Pulsing-in Time (µs)',fontsize=20)
plt.ylabel('Pumping-out Time (s)',fontsize=20)
plt.tight_layout()
plt.savefig(f"Plotting/{rgnt}.png",dpi=600)
plt.show()

#MOP_1 0 -> 35 -> 61 (1.4,70), 0 -> 12 - > 53 (1.5, 80)
#TMB_0 6 -> 15 -> 58
#TDMAB 7 -> 10 -> 23 (3,170)