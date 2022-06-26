import numpy as np

mop = np.load("Plotting_and_Processing/MOP_SI.npy", allow_pickle = True)
tmb = np.load("Plotting_and_Processing/TMB_SI.npy", allow_pickle = True)
tdmab = np.load("Plotting_and_Processing/TDMAB_SI.npy", allow_pickle = True)

f = open("Plotting_and_Processing/MOP_SI.csv","w")
for i in mop:
    if i[3] == -100.0:
        if len(i) == 5:
            f.write(f"{int(i[0])},{i[1]},{int(i[2])},{i[4]-2.5},{i[4]}\n")
        else:
            f.write(f"{int(i[0])},{i[1]},{int(i[2])},{round(i[4]-2.5,4)},{round(i[4],4)},{round(i[5],4)},{round(i[6],4)},{round(i[7],4)}\n")
    else:
        if len(i) == 5:
            f.write(f"{int(i[0])},{i[1]},{int(i[2])},{i[3]},{i[4]}\n")
        else:
            f.write(f"{int(i[0])},{i[1]},{int(i[2])},{round(i[3],4)},{round(i[4],4)},{round(i[5],4)},{round(i[6],4)},{round(i[7],4)}\n")
f.close()

f = open("Plotting_and_Processing/TMB_SI.csv","w")
for i in tmb:
    if i[3] == -100.0:
        if len(i) == 5:
            f.write(f"{int(i[0])},{i[1]},{int(i[2])},{i[4]-2.5},{i[4]}\n")
        else:
            f.write(f"{int(i[0])},{i[1]},{int(i[2])},{round(i[4]-2.5,4)},{round(i[4],4)},{round(i[5],4)},{round(i[6],4)},{round(i[7],4)}\n")
    else:
        if len(i) == 5:
            f.write(f"{int(i[0])},{i[1]},{int(i[2])},{i[3]},{i[4]}\n")
        else:
            f.write(f"{int(i[0])},{i[1]},{int(i[2])},{round(i[3],4)},{round(i[4],4)},{round(i[5],4)},{round(i[6],4)},{round(i[7],4)}\n")
f.close()

f = open("Plotting_and_Processing/TDMAB_SI.csv","w")
for i in tdmab:
    if i[3] == -100.0:
        if len(i) == 5:
            f.write(f"{int(i[0])},{i[1]},{int(i[2])},{i[4]-2.5},{i[4]}\n")
        else:
            f.write(f"{int(i[0])},{i[1]},{int(i[2])},{round(i[4]-2.5,4)},{round(i[4],4)},{round(i[5],4)},{round(i[6],4)},{round(i[7],4)}\n")
    else:
        if len(i) == 5:
            f.write(f"{int(i[0])},{i[1]},{int(i[2])},{i[3]},{i[4]}\n")
        else:
            f.write(f"{int(i[0])},{i[1]},{int(i[2])},{round(i[3],4)},{round(i[4],4)},{round(i[5],4)},{round(i[6],4)},{round(i[7],4)}\n")
f.close()