import csv
import glob
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
import scipy
from sklearn.linear_model import LinearRegression
from scipy import stats
from tabulate import tabulate

folder_path = "/Users/stephanieruch/Desktop/K_FINAL DATA /K_CSV_Speed"
folder_path2= "/Users/stephanieruch/Desktop/K_FINAL DATA /K_CSV_Dis"

def read_raw_data(raw_data):
    d_min = []
    n = []
    s = []
    with open(raw_data) as csv_file:
        readCSV = csv.reader(csv_file)
        for line in csv_file:
            name, distance_min, speed, none = line.split(";")
            distance_min = float(distance_min)
            d_min.append(distance_min)
            speed=float(speed)
            s.append(speed)
            n.append(name)
    return (n,d_min,s)

def Speed_Distance(name):
    speed = []
    distance = []
    for i in range(0, len(name)):
        s = name[i].split("_")[1].split("=")[-1]
        s = float(s)
        speed.append(s)
        d = name[i].split("_")[2].split("=")[-1]
        d = float(d)
        distance.append(d)
    return speed, distance

def Color(dist):
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
def Color2(speed):
    if speed == 0.1:
        l= "darkblue"
    elif speed == 0.3:
        l= "royalblue"
    elif speed == 0.5:
        l= "dodgerblue"
    elif speed == 0.7:
        l= "darkviolet"
    elif speed == 0.9:
        l = "indigo"
    elif speed == 1.5:
        l = "fuchsia"
    else:
        l = "plum"

    return l

def main():
    files = glob.glob(folder_path + "/*.csv")
    files.sort()

    fig, (ax) = plt.subplots()
    fig.set_size_inches(12, 7)
    ax.plot(0, 100, "^", color="r", markersize=5, label="$y_{2 d=0 mm/s}$")

    d_0 =[]

    for x in files:
        name,distance_min, slope = read_raw_data(x)
        speed,distance = Speed_Distance(name)

        distance = np.array(distance)
        distance = distance.reshape(-1, 1)
        slope = np.array(slope)
        slope = slope.reshape(-1, 1)

        lin_reg = LinearRegression()
        lin_reg.fit(distance, slope)
        Y_pred = lin_reg.predict(distance)

        ax.set_xlabel("Distance [mm]")
        ax.set_ylabel("Slope[V]")
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_minor_locator(MultipleLocator(0.1))
        ax.xaxis.set_major_locator(MultipleLocator(0.005))
        ax.xaxis.set_minor_locator(MultipleLocator(0.001))
        ax.xaxis.label.set_size(15)
        ax.yaxis.label.set_size(15)

        spe = speed[0]
        p = Color2(spe)
        spe = str(spe)

        ax.plot(distance, slope, '^', markersize=3, color="k")
        ax.plot(distance, Y_pred, color= p, linewidth=1,linestyle="--", label="v = "+spe + "mms$^{-1}$")
        slope, intercept, r_value, p_value, std_err = scipy.stats.mstats.linregress(distance,slope)

        ax.plot(0,intercept, "^", color="r", markersize =5)
        d_0.append(intercept)
        ax.legend(ncol=1, facecolor="white", edgecolor="k", framealpha=1)
        plt.ylim(0, 10)
        #plt.close(fig)
    plt.show()

    files2 = glob.glob(folder_path2 + "/*.csv")
    files2.sort()
    d_zero = [0.1, 0.3,0.5,0.7,0.9,1.5,2.0]
    fig2, (ax2) = plt.subplots()
    fig2.set_size_inches(12, 7)
    ax2.set_xlabel("Velocity [mms$^{-1}$]")
    ax2.set_ylabel("Slope[Vs$^{-1}$]")

    d_zero = np.array(d_zero)
    d_zero = d_zero.reshape(-1, 1)
    d_0 = np.array(d_0)
    d_0 = d_0.reshape(-1, 1)

    lin_reg = LinearRegression()
    lin_reg.fit(d_zero, d_0)
    Y_pred3 = lin_reg.predict(d_zero)
    #ax2.plot(d_zero, Y_pred3, color="k",label= "d= 0.0", linestyle="--", linewidth=1)

    d_0 = [-0.20538589049354838, -0.6441532727596775, -1.0857404061596774, -1.5480194283483868, -2.140878591104839,
           -3.9790906839442166, -5.363925969065869]
    ve = [0.1, 0.3, 0.5, 0.7, 0.9, 1.5, 2.0]

    ve = np.array(ve)
    ve = ve.reshape(-1, 1)

    d_0 = np.array(d_0)
    d_0 = d_0.reshape(-1, 1)

    lin_reg = LinearRegression()
    lin_reg.fit(ve, d_0)
    Y_pred0 = lin_reg.predict(ve)

    ax2.plot(ve, Y_pred0, linewidth=1, linestyle="--", label="d = 0.0 mm", color="r")
    ax2.plot(ve, d_0, 'o', markersize=3, color="r")

    for x in files2:
        name2, distance_min2, slope2 = read_raw_data(x)
        slope2 = [x* -1 for x in slope2]
        speed2, distance2 = Speed_Distance(name2)

        speed2 = np.array(speed2)
        speed2 = speed2.reshape(-1, 1)
        slope2 = np.array(slope2)
        slope2 = slope2.reshape(-1, 1)

        lin_reg = LinearRegression()
        lin_reg.fit(speed2, slope2)
        Y_pred2 = lin_reg.predict(speed2)

        dist = distance2[0]
        l = Color(dist)
        dis=str(dist)
        if dist == 0.005 or dist == 0.01 or dist == 0.015 or dist == 0.02 or dist == 0.025:
            ax2.plot(speed2, Y_pred2,linewidth=1,linestyle ='--', color = l, label = "d= " +dis +"mm")
            ax2.plot(speed2, slope2, '^', markersize=3, color="k") #label= "d= " +distance)


        #ax2.plot(d_zero, d_0, '^', markersize=3, color="r", label="d = 0 ")

        if dist ==0.001:
            ax2.plot(speed2, Y_pred2, color="k", label= "d = 0.001")
            m3, intercept3 , r_value, p_value, std_err= scipy.stats.mstats.linregress(speed2, slope2)
        ax2.yaxis.set_major_locator(MultipleLocator(1))
        ax2.yaxis.set_minor_locator(MultipleLocator(0.1))
        ax2.xaxis.set_major_locator(MultipleLocator(0.1))
        ax2.xaxis.set_minor_locator(MultipleLocator(0.01))
        ax2.xaxis.label.set_size(15)
        ax2.yaxis.label.set_size(15)
        ax2.legend(ncol=1, facecolor="white", edgecolor="k",framealpha=1)






    plt.show()


main()

