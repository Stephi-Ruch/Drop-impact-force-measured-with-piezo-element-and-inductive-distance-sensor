import csv
import glob
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
import scipy
from sklearn.linear_model import LinearRegression
from scipy import stats

folder_path1= "/Users/stephanieruch/Desktop/BA/pythonProject_backup_10.08.2021/1. K2_TA_DS_Kalibrierung/2. CSV Datein für Python"
folder_path = "/Users/stephanieruch/Desktop/BA/pythonProject_backup_10.08.2021/1. K2_TA_DS_Kalibrierung/1. Raw Daten und Bearbeite Excel nach v"
csv_file = "/Users/stephanieruch/Desktop/BA/pythonProject_backup_10.08.2021/1. K2_TA_DS_Kalibrierung/2.1. Find v=0.0.csv"

def read_data(csv_file):
    y = []
    with open(csv_file) as csv_file:
        for line in csv_file:
            distance, y_int, nothing = line.split(";")
            y_int = float(y_int)
            y.append(y_int)
    return (y)

def lin_funcion(slope, int, x):
    return slope * x + int
def distance_function(y_volt, slope, y_int):
    return (y_volt/slope)-y_int
def Average(lst):
    return sum(lst) / len(lst)
def Color(title):
    dist = title.split("=")[-1]
    dist= float(dist)
    if dist == 0.025:
        l= "darkblue"
    elif dist == 0.02:
        l= "royalblue"
    elif dist == 0.015:
        l= "dodgerblue"
    elif dist == 0.01:
        l= "darkviolet"
    elif dist == 0.005:
        l = "plum"
    else:
        l="fuchsia"
    return l
def read_raw_data1(raw_data):
    d_min = []
    n = []
    with open(raw_data) as csv_file:
        readCSV = csv.reader(csv_file)
        for line in csv_file:
            name, distance_min,  none = line.split(";")
            distance_min = float(distance_min)
            d_min.append(distance_min)
            name=float(name)
            n.append(name)
    return (n,d_min)
def read_raw_data(raw_data):
    d_min = []
    with open(raw_data) as csv_file:
        for line in csv_file:
            name, distance_min,  none = line.split(";")
            distance_min = float(distance_min)
            d_min.append(distance_min)
    return (d_min)

def main1():
    files = glob.glob(folder_path1 + "/*.csv")
    files.sort()
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 7)

    ax.plot(0, 0, "^", color="r", label= "$y_{v = 0 mm}$", markersize=5)
    ax.plot(0, 0, 'o', markersize=2, color="k", label="Voltage Output")

    for x in files:
        speed,distance_min = read_raw_data1(x)
        title = x.split(" ")[-1].split(".csv")[0]

        ax.plot(speed, distance_min, 'o', markersize=2,color="k")
        speed = np.array(speed)
        speed = speed.reshape(-1, 1)
        distance_min = np.array(distance_min)
        distance_min = distance_min.reshape(-1, 1)

        lin_reg = LinearRegression()
        lin_reg.fit(speed, distance_min)
        Y_pred = lin_reg.predict(speed)

        ax.set_xlabel("Velocity [mms$^{-1}$]")
        ax.set_ylabel("Voltage Output [V]")

        l =Color(title)
        ax.plot(speed, Y_pred, color=l, linewidth=1,linestyle ="--", label= title +" mm")

        slope, intercept, r_value, p_value, std_err = scipy.stats.mstats.linregress(speed,distance_min)

        ax.set_ylim(-1.1,-0.6)
        print(title,round(intercept,5), round(r_value,5))
        ax.plot(0,intercept, "^", color="r")
        ax.legend(loc=0, prop={'size': 10})
        ax.tick_params(direction="in")
        ax.xaxis.label.set_size(15)
        ax.yaxis.label.set_size(15)
        ax.legend(ncol=1, facecolor="white", edgecolor="k",framealpha=1)
    plt.show()
main1()

def main():
    print("")
    y_int = read_data(csv_file)
    dis = [0.001, 0.005, 0.010, 0.015, 0.020, 0.025]
    fig, (ax) = plt.subplots()
    fig.set_size_inches(12, 7)

    dis = np.array(dis)
    dis = dis.reshape(-1, 1)
    y_int = np.array(y_int)
    y_int = y_int.reshape(-1, 1)

    lin_reg = LinearRegression()
    lin_reg.fit(dis,y_int)
    Y_pred = lin_reg.predict(dis)

    slopy =[]
    int = []

    slope, intercept, r_value, p_value, std_err = scipy.stats.mstats.linregress(dis,y_int)
    print("v=0.0",slope, intercept)
    slopy.append(slope)
    int00 = intercept

    ax.set_xlabel("Distance [mm]")
    ax.set_ylabel("Voltage output [V]")
    ax.xaxis.set_major_locator(MultipleLocator(0.005))
    ax.xaxis.set_minor_locator(MultipleLocator(0.001))
    ax.yaxis.set_major_locator(MultipleLocator(0.1))
    ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    ax.xaxis.label.set_size(15)
    ax.yaxis.label.set_size(15)
    ax.tick_params(direction="in")
    plt.xlim(-0.002,0.027)
    plt.ylim(-1.05,-0.55)

    plt.plot(0, 0, 'o', markersize=3, color="k", label ="Votage Output")
    plt.plot(dis, y_int, "^", color="r", markersize=3, label = "$y_{v=0 mm/s} $")
    plt.plot(dis, Y_pred, color="k", linewidth=1, linestyle="--", label='v=0 mms$^{-1}}$ *')

    files = glob.glob(folder_path + "/*.csv")
    files.sort()
    for x in files:
        signal_min = read_raw_data(x)

        lable = x.split("/")[-1].split(" ")[-1].split(".csv")[0]
        distance = [0.001, 0.005, 0.010, 0.015, 0.020, 0.025]

        distance = np.array(distance)
        distance = distance.reshape(-1, 1)
        signal_min = np.array(signal_min)
        signal_min = signal_min.reshape(-1, 1)

        lin_reg = LinearRegression()
        lin_reg.fit(distance, signal_min)
        Y_pred = lin_reg.predict(distance)

        plt.plot(distance, Y_pred, linewidth=1, linestyle="--", label= lable + " mms$^{-1}$")
        plt.plot(distance, signal_min, 'o', markersize=3,color="k")

        slope, intercept, r_value, p_value, std_err = scipy.stats.mstats.linregress(distance, signal_min)

        print(lable,slope,intercept)

        slopy.append(slope)
        int.append(intercept)

    a =[0,0,0,0,0,0,0]
    plt.plot(a, int, "^", color="dodgerblue", markersize=5, label=" $y_{d = 0 mm}$")
    y0 = int[0]
    plt.plot(0,y0,"^",color ="g", markersize =5, label="$y_{d = 0 mm, v = 0 mm/s}$")
    ax.legend(ncol=1, facecolor = "white", edgecolor ="k", framealpha=1)
    plt.show()

    # Einfacher ein Array zu machen das alle v enthählt
    v = [0.1,0.3,0.5,0.7,0.9,1.5,2.0]

    fig, ax3 = plt.subplots()
    fig.set_size_inches(12, 7)
    ax3.xaxis.set_major_locator(MultipleLocator(0.2))
    ax3.xaxis.set_minor_locator(MultipleLocator(0.1))
    ax3.yaxis.set_major_locator(MultipleLocator(0.05))
    ax3.yaxis.set_minor_locator(MultipleLocator(0.01))
    ax3.set_xlabel("Velocity [mm/s]")
    ax3.set_ylabel("Y-Interecpts [V]")
    ax3.plot(v, int, "^", color="r", markersize=5,label= "$y_{d=0 mm} $")
    ax3.plot(0, int00, "^", color="green", markersize=5,label= "$y_{d = 0 mm, v = 0 mm/s}$")
    ax3.xaxis.label.set_size(15)
    ax3.yaxis.label.set_size(15)

    int = np.array(int)
    int = int.reshape(-1, 1)
    v = np.array(v)
    v = v.reshape(-1, 1)
    lin_reg.fit(v, int)

    Y_pred2 = lin_reg.predict(v)

    ax3.plot(v, Y_pred2, color="k",linewidth=1, label = "Linear Regression of Y-Intercepts")
    ax3.legend(ncol=1, facecolor = "white", edgecolor ="k", framealpha=1)

    m3, intercept3, r_value3, p_value3, std_err3 = scipy.stats.mstats.linregress(v, int)

    print("")
    print("Slope")
    print("Data:",slopy)
    print("Average:",Average(slopy))
    slopy=np.array(slopy)
    std_slope=np.std(slopy)
    print("std:",std_slope)
    print("")
    print("Intercepts line Equation: y =", m3,"x + ", intercept3)
    print(int00)


    plt.show()
main()






