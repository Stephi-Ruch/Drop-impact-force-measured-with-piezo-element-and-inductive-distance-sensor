import glob
import math

import matplotlib.pyplot as plt
import pandas as pd
import scipy
from matplotlib.ticker import MultipleLocator
from scipy.signal import butter,filtfilt
import numpy as np
from sklearn.linear_model import LinearRegression

## Area of TA Application
a2 = 2.48 *0.001 ## durchmesser mm zu m
a2 = a2/2
a2 = (a2**2)*math.pi
print(a2)


## Hight of Piezo
h = 0.44 ## in mm

folder_path = "/Users/stephanieruch/Desktop/BA/*Jetter + Piezo + Neu DS /k_Piezo_Kallibierung_mit_TA/TA E-Moldul CSV"



def max_point(distance,mean_force):
    max_force = max(mean_force)
    max_distance_force = mean_force.index(max_force)
    max_distance_force = distance[max_distance_force]
    return [max_distance_force,max_force]

def Average(lst):
    return sum(lst) / len(lst)

def new_signal_def(mean_force,distance):
    ## die ersten Zwei Daten pünkte werden entfernt, diese haben eine aufällig andere staeigung zu den andern. Ea könnte sich dabei um den Para-Film handeln
    ## Zur E-Modul auswertung, werden nur distancen 0.2 mm über berücksichtigt, die andern datensätze haben zu wenig punkte
    ## Letzten punkt auch entferenen von array, auch aufalled andere steigung, vieleicht einfach bewegungs inkremente des TA nicht in 0.1mm

    signal_distance = []
    signal = []
    for i in range(0, len(mean_force)):
        if distance[i] > distance[i-1]:
            signal.append(mean_force[i])
            signal_distance.append(distance[i])

    return [signal_distance,signal]

def read_csv(csv_file):
    go = False
    f = []
    d = []
    t = []
    with open(csv_file) as csv:
        csv = csv.read().splitlines()
        for line in csv:
            if go == True:
                force, distance, time = line.split(";")
                force = float(force)
                distance = float(distance)
                time = float(time)
                f.append(force)
                d.append(distance)
                t.append(time)
            if line.startswith("0"):
                go = True
    return [f,d,t]

def main_raw():
    files = glob.glob(folder_path + "/*.csv")
    files.sort()
    print("")

    slopy =[]

    fig, ax1 = plt.subplots()
    fig.set_size_inches(8,8)

    for x in files:
        force, distance, time = read_csv(x)

        x = x.split("/")[-1]
        v= x.split("_")[0].split("=")[1]
        d=x.split("_")[1].split("=")[1].split(".csv")[0]

        #signal_distance, signal = new_signal_def(mean_force, distance)
        signal_distance, signal = new_signal_def(force, distance)

        force_N = [x * 0.00981 for x in signal]
        stress = [x / a2 for x in force_N]
        strain = [x / h for x in signal_distance]

        ax1.plot(strain, stress, "^", color ="k", markersize= 3 )

        strain.remove(strain[-1])
        stress.remove(stress[-1])

        strain = np.array(strain)
        strain= strain.reshape(-1,1)
        stress = np.array(stress)
        stress=stress.reshape(-1,1)

        lin_reg = LinearRegression()
        lin_reg.fit(strain, stress)
        Y_pred2 = lin_reg.predict(strain)

        slope, intercept, r_value_of_lin_reg, p_value_of_lin_reg, std_err = scipy.stats.mstats.linregress(strain, stress)
        slopy.append(slope)

        ax1.plot(strain, Y_pred2, label = "v="+ v + " d=" + d, linestyle ="--")
        ax1.xaxis.set_major_locator(MultipleLocator(0.01))
        ax1.xaxis.set_minor_locator(MultipleLocator(0.001))
        ax1.yaxis.set_major_locator(MultipleLocator(500))
        ax1.yaxis.set_minor_locator(MultipleLocator(50))
        ax1.set_xlabel("W/h [-]")
        ax1.set_ylabel("F/A [N/m$^{2}$]")
        ax1.xaxis.label.set_size(15)
        ax1.yaxis.label.set_size(15)
        ax1.legend(loc=0, prop={'size': 10})
        #plt.close(fig)

    plt.show()
    av = Average(slopy)
    print(av)
    slopy = np.array(slopy)
    std = np.std(slopy)
    print(std)
    print((std/av)*100)



main_raw()
