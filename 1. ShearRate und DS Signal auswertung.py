import glob
import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from numpy.fft import rfft, rfftfreq
from scipy.signal import butter, filtfilt

folder_path = "/Users/stephanieruch/Desktop/Daten mit Neuer Düsse 600 Kopie/2.b.iii_Cacao_600_temp=32.3/2biii t2=10000"
#folder_path = "/Users/stephanieruch/PycharmProjects/pythonProject/1. K2_TA_DS_Kalibrierung/1. Raw Daten und Bearbeitete Excel _nach_d/K2_d=0.025"

def Shear_rate(pressure, t_h ,viscosity):
    radius = 300  # In µm to m
    radius = radius * 1e-6

    area = math.pi * radius ** 2

    # Difference form valve to atmosphere, in bar to pa
    pressure = pressure -1
    pressure = pressure * 100000

    # Holding time µs to s
    t_h = t_h * 1e-6

    # Length of Die for mm to m
    length = 1.1
    length = length / 1000

    velocity = (math.pi * radius ** 4 * pressure) / (8 * viscosity * length * area)
    print(velocity)
    # volumeflow = velocity * area
    volume_drop = velocity * area * t_h
    diametere_drop = 2 * (((3 * volume_drop) / (4 * math.pi))**(1/3))

    shear_rate = velocity / diametere_drop
    return shear_rate,velocity, volume_drop

def Force(velocity,drop_volume, x):

    #print(drop_volume)

    x = x.split("/")[-1]
    if x.startswith("2"):
        mass = drop_volume * 0.9
    else:
        mass = drop_volume * 1

    time = 0.5 # in s
    acceleration = velocity/time

    force = mass* acceleration

    #estimate_w = (force /(181.586*1000))*1000 # in mm
    estimate_w = ((force * 0.44) / (4.830512e-06 * 16648.40830404204))  # in mm
    return force, estimate_w

def butter_lowpass_filter(data, cutoff, fs, order):
    nyq = 8000 / 2
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def min_point(time, p):
    min_rolling_mean = min(p)
    min_time = p.index(min_rolling_mean)
    min_time = time[min_time]
    return [min_time, min_rolling_mean]
def max_point(time, p):
    max_rolling_mean = max(p)
    max_time = p.index(max_rolling_mean)
    max_time = time[max_time]
    return [max_time, max_rolling_mean]

def find_av(dis_sen,start,end):
    d = []
    sum_d = 0
    for i in range(start, end):
        d.append(dis_sen[i])
    for i in range(0, len(d)):
        sum_d = sum_d + d[i]
    av_start_d = sum_d / len(d)
    return [av_start_d]

def Slope(time, dis_sen):
    t_min, d_min = min_point(time, dis_sen)

    s = []
    t_slope = []
    for i in range(0, len(time)):
        if time[i] <= t_min:
            if dis_sen[i] >= 0.2 * d_min and dis_sen[i +5] <= 0.2 * d_min:
                s.append(dis_sen[i])
                t_slope.append(time[i])

    start = float(s[0])
    start_time = t_slope[0]

    slope = (d_min - start)/(t_min-start_time)

    return slope, start, start_time

def Materials(x):
    x = x.split("/")[-1]
    if x.startswith("1"):
        name = "milliQ Water"
        viscosity = 0.00089
        h = "lightblue"
    elif x.startswith("2a"):
        name = "Cacao Butter"
        viscosity = 0.8
        h = "indianred"
    elif x.startswith("2b"):
        name = "Cacao Butter"
        viscosity = 0.8
        h = "tomato"
    elif x.startswith("2c"):
        name = "Cacao Butter"
        viscosity = 0.8
        h = "orange"
    elif x.startswith("3.bi"):
        name = "PEO solution"
        viscosity = 0.004
        h = "mediumseagreen"
    elif x.startswith("3bii"):
        name = "PEO solution"
        viscosity = 0.097
        h = "limegreen"
    elif x.startswith("3biii_p"):
        name = "PEO solution"
        viscosity = 1.500
        h = "lightgreen"
    elif x.startswith("Sch"):
        name = "Cacao Butter Foam"
        h = "k"

    return [name, viscosity]

def Frequency_Analyis(x,y):
    n = len(x)
    y = rfft(y)
    x = rfftfreq(n, 1 / 8000)
    return [x,np.abs(y)]

def Parameter(x):
    pressure = x.split("/")[-1].split("_")[1].split("=")[-1]
    pressure = float(pressure)
    t_h = x.split("/")[-1].split("_")[2].split("=")[-1]
    t_h = float(t_h)
    return [pressure,t_h]

def read_csv(csv_file):
    go = False
    tta = []
    cta2 = []
    cta1 = []
    with open(csv_file) as csv:
        csv = csv.read().splitlines()
        for line in csv:
            if go == True:
                time, channel_1, channel_2 = line.split(",")
                channel_2 = float(channel_2)
                channel_1 = float(channel_1)
                time = float(time)
                tta.append(time)
                cta2.append(channel_2)
                cta1.append(channel_1)
            if line.startswith("Time"):
                go = True
    return [tta, cta1, cta2]

def Main():
    files = glob.glob(folder_path + "/*.csv")
    files.sort()
    print("")
    for x in files:
        t, p, d = read_csv(x)

        name, viscosity = Materials(x)
        pressure, t_h = Parameter(x)
        shear_rate,velocity , drop_volume= Shear_rate(pressure, t_h, viscosity)
        force, esitimate_w = Force(velocity, drop_volume, x)
        q = x.split("_")[-1]

        dis_sen = []
        time = []
        for i in range(5000, len(d)):
            dis_sen.append(d[i])
            time.append((t[i]))

        dis_sen = butter_lowpass_filter(dis_sen, 800, 8000, 2)  # Butter Filter to remove noise from Piezo
        # dis_sen = numpy.array(dis_sen)

        frequency, intensity = Frequency_Analyis(time, dis_sen)

        av_start_d = find_av(dis_sen, 0, 1500)
        dis_sen = [x - av_start_d for x in dis_sen]

        t_min, d_min = min_point(time, dis_sen)

        d_s =[]
        ti=[]
        for i in range(0, len(time)):
            if time[i]<t_min:
                ti.append(time[i])
                d_s.append(dis_sen[i])

        t_max, d_max = max_point(ti, d_s)

        slope, start, start_time = Slope(time, dis_sen)

        ## Main Figure
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches(12, 7)
        fig.suptitle(x.split("/")[-1])

        ax1.axhline(y=0, color="r", linewidth=1)
        ax1.set_title('(A)')
        ax1.plot(time, dis_sen, color="k", linewidth=1, label="Filterd Distance Sensor Signal")
        ax1.plot(start_time, start, "o", color="dodgerblue", label="Maximum/Minimum of\n Original Piezo Signal")
        ax1.plot(t_max, d_max, "o", color="r", label="Maximum/Minimum of\n Original Piezo Signal")
        ax1.plot(t_min, d_min, "o", color="r")
        ax1.set_xlabel("Time [s]")
        ax1.set_ylabel("DS Signal [v]")
        ax1.legend(loc=0, prop={'size': 10})
        #ax1.set_ylim(-0.0090, 0.0129)


        ax2.set_title('(B)')
        ax2.plot(frequency, intensity, color="dodgerblue", linewidth=1,
                 label="Frequency Filterd Distance \nSensor Signal")
        ax2.yaxis.set_major_locator(MultipleLocator(0.5))
        ax2.yaxis.set_minor_locator(MultipleLocator(0.1))
        ax2.xaxis.set_major_locator(MultipleLocator(500))
        ax2.xaxis.set_minor_locator(MultipleLocator(100))
        ax2.set_xlabel("Frequency [Hz]")
        ax2.set_ylabel("Intensity a.u.")
        ax2.legend(loc=0, prop={'size': 10})
        ax2.set_ylim(0, 3)
        plt.close(fig)
        #plt.show()

        d_max = d_max[0]
        d_min = d_min[0]
        slope = slope[0]

        table_line = []
        table_line.append(x.split("/")[-1])
        #table_line.append(d_max)
        #table_line.append(0)
        #table_line.append(d_min)
        table_line.append(slope)
        #table_line.append(0)
        #table_line.append(esitimate_w)
        table_line.append(0)
        table_line.append(0)
        #table_line.append(shear_rate)

        table_line = ','.join(str(x) for x in table_line)
        #print(table_line)

    # print(viscosity)


Main()

""""
#ax1.xaxis.set_major_locator(MultipleLocator(0.005))
  #ax1.xaxis.set_minor_locator(MultipleLocator(0.001))
  # ax1.xaxis.set_major_locator(MultipleLocator(0.5))
  # ax1.xaxis.set_minor_locator(MultipleLocator(0.1))
  #ax1.yaxis.set_major_locator(MultipleLocator(0.0025))
  #ax1.yaxis.set_minor_locator(MultipleLocator(0.0005))
  
    #ax1.set_xlim(-61.820, -61.795)

"""