import glob
import matplotlib.pyplot as plt
import numpy as np
import scipy
from matplotlib.ticker import MultipleLocator
from scipy.signal import butter, filtfilt
from sklearn.linear_model import LinearRegression
from scipy.fft import rfft, rfftfreq

folder_path = "/Users/stephanieruch/Desktop/Daten mit Neuer Düsse 600 Kopie/1.b_Wasser_600/1b t2=1000"

def butter_lowpass_filter(data, cutoff, fs, order):
    nyq = 8000 / 2
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def butter_highpass_filter(data, cutoff, fs, order):
    nyq = 8000 / 2
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
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

def function(A0, a, x):
    return A0 * np.exp(a * x)
def Average(lst):
    return sum(lst) / len(lst)

def Piezo_null(piezo):
    first_1000_data_points = []
    for i in range(0,1000):
        first_1000_data_points.append(piezo[i])
    piezo_0 = Average(first_1000_data_points)
    return [piezo_0]

def Finding_max_min_Residuals(x,y,Y_pred,percent):
    residual = []
    residual_t = []
    for i in range(0, len(y)):
        r = (y[i] - Y_pred[i])
        r = r[0]
        residual.append(r)
        tre = x[i]
        # tre=tre[0]
        residual_t.append(tre)

    res_mins = []
    res_t_mins = []
    for i in range(0, len(residual) - 2):
        if (residual[i] > residual[i + 1]) and residual[i + 1] < residual[i + 2]:
            res_mins.append(residual[i + 1])
            res_t_mins.append(residual_t[i + 1])

    res_look = []
    res_t_look = []
    for i in range(0, len(res_mins)):
        if res_mins[i] < percent:
            res_look.append(res_mins[i])
            res_t_look.append((res_t_mins[i]))

    return [residual,residual_t, res_mins,res_t_mins,res_look,res_t_look]
def av_abs_residual_error(n,y_pred,y_act):
    s=0
    for i in range(0,n):
        sum = abs(y_act[i]-y_pred[i])
        s=s+sum
    return (1/n)*s

def linear_regression(time,y):
    x = time
    y_ln = np.log(y)
    y_ln= np.array(y_ln)
    y_ln = y_ln.reshape(-1, 1)
    x = np.array(x)
    x = x.reshape(-1, 1)

    lin_reg = LinearRegression()
    lin_reg.fit(x, y_ln)
    Y_pred = lin_reg.predict(x)
    return [y_ln,Y_pred]

def Piezo_cut_out(time, piezo):
    time_max, p_max = max_point(time, piezo)

    t = []
    p = []
    for i in range(0, 5000):
        if time_max <= time[i]:
            t.append(time[i])
            p.append(piezo[i])

    return(t,p, time_max, p_max)

def Oscilation_Analyisis(t,p, time_max, p_max):

    p = butter_highpass_filter(p, 1500, 8000, 2)  # Butter Filter to remove noise from Piezo
    #p = butter_lowpass_filter(p, 1500, 8000, 2)  # Butter Filter to remove noise from Piezo

    # This Low and High Pass chosen, b/c it is where the highest peak starts ascending and
    # Short evaluation of std error, this seems to be lowest, or constantly low at this setting - lower than when only low-pass filter was applied
    time_max = 0

    t_o_min = []
    o_min = []
    t_o_max = []
    t_o_max.append(time_max)
    o_max = [p_max]

    for i in range(0, len(p) - 2):
        if (p[i] > p[i + 1]) and p[i + 1] < p[i + 2]:
            o_min.append(p[i + 1])
            t_o_min.append(t[i + 1])
        if (p[i] < p[i + 1]) and (p[i + 1] > p[i + 2]):
            o_max.append(p[i + 1])
            t_o_max.append(t[i + 1])
    
    t_o_min.remove(t_o_min[0])
    o_max.remove(o_max[0])
    t_o_max.remove(t_o_max[0])
    o_min.remove(o_min[0])

    t_osc_max, osc_max = max_point(t_o_max, o_max)

    osc = [osc_max]
    t_osc = [t_osc_max]
    for i in range(1, 50):
        if o_max[i] > 0.01 * osc_max:
            osc.append(o_max[i])
            t_osc.append(t_o_max[i])

    o = []
    t_o = []
    for i in range(0, len(t_osc)):
        if (t_osc[i] >= t_osc_max):
            o.append(osc[i])
            t_o.append(t_osc[i])

    t_o = [x - min(t_o) for x in t_o]
    p=p.tolist()
    ti,pi=max_point(t,p)
    t = [x - ti for x in t]

    frequency_check_data = []
    frequency_check_time = []
    for i in range(0, len(p)):
        if t[i] >= t_o[0]  and t[i] <= t_o[-1] :
            frequency_check_time.append(t[i])
            frequency_check_data.append(p[i])

    frqu_t = frequency_check_time
    freq_t, frq_max = max_point(frequency_check_time,frequency_check_data)
    frequency_check_time = [x - freq_t for x in frequency_check_time]
    return [o_max,p,t,t_o,o,frequency_check_time,frequency_check_data,frqu_t]

def Frequency_Analyis(x,y):
    ## frquency Anaysis
    n = len(x)
    yd = rfft(y)
    xf = rfftfreq(n, 1 / 8000)
    yd = abs(yd)
    return [xf,yd]
def top_Freqency_Intensiry(frequency,intesnity):
    intesnity = intesnity.tolist()
    peak_intesnity = []
    for i in range(0, len(intesnity) - 2):
        if (intesnity[i] < intesnity[i + 1]) and intesnity[i + 1] > intesnity[i + 2]:
            peak_intesnity.append(intesnity[i+1])

    three_peaks = []
    three_index = []
    for i in range(0, 4):
        intesnity_max = max(peak_intesnity)
        three_peaks.append(intesnity_max)
        ind = intesnity.index(intesnity_max)
        three_index.append(ind)
        peak_intesnity.remove(intesnity_max)

    fq1 = frequency[three_index[0]]
    fq2 = frequency[three_index[1]]
    fq3 = frequency[three_index[2]]
    fq4 = frequency[three_index[3]]
    return [three_peaks[0],fq1,three_peaks[1],fq2,three_peaks[2],fq3,three_peaks[3],fq4]

def Name_lable(x):
    x = x.split("/")[-1]

    if x.startswith("2"):
        name = "Cacao Butter"
    elif x.startswith("3"):
        name = "PEO solution"
    elif x.startswith("1"):
        name = "milliQ Water"
    else:
        name = "Cacao Butter Foam"
    lable_t2 = x.split("_")[2].split("=")[-1]
    lable_p = x.split("_")[1]
    return [name, lable_t2, lable_p]

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

def main_raw():
    files = glob.glob(folder_path + "/*.csv")
    files.sort()
    print("")
    text_file = open("../PIEZO Oscilation Analysis.csv", "w")
    text_file.write("")
    text_file.close()
    print( "Name","Residual_Error", "Piezo_Max","Av_Piezo_Max", "Piezo_Min", "Av_Piezo_Min","Oscillation_Max", "Av_Oscillation_Max","A0","Av_A0", "Slope", "Av_Slope", "Fq1","Int1","Fq2","Int2", "Fq3","Int3", "Fq4","Int4")

    fig3,ax3= plt.subplots()
    fig3.set_size_inches(10, 8)
    fig3.suptitle("Piezo Siganl", fontsize=16)
    plt.close(fig3)

    for x in files:
        ti, pi, dis_sen = read_csv(x)

        piezo = []
        time = []
        for i in range(1500, len(pi)):
            time.append(ti[i])
            piezo.append(pi[i])

        piezo_0 = Piezo_null(piezo)
        piezo_0 = piezo_0[0]
        piezo = [x - piezo_0 for x in piezo]

        ## Maximum and minimum of Piezo Siganl
        ti_max, pi_max = max_point(time, piezo)
        time = [x - ti_max for x in time]
        ti_min, pi_min = min_point(time, piezo)
        ti_max, pi_max = max_point(time, piezo)

        t, p, time_max, p_max = Piezo_cut_out(time, piezo)
        name, lable_t2, lable_p = Name_lable(x)

        ## Cutting Piezo Signal, finding peaks of Oscilaiton and the actual Oscialtaion
        osc_max, p, t, t_o, o, oscilaion_time, oscilation, frqu_t= Oscilation_Analyisis(t, p,time_max,p_max)

        ## Linear Regression of Oscilations Peaks in Piezo Signal
        y, Y_pred = linear_regression(t_o,o)

        ## Figure 3 Showing Linear Regression of Oscilation
        fig1, ax11 = plt.subplots()
        fig1.set_size_inches(10, 7)
        ax11.plot(t_o, Y_pred, color="dodgerblue", linewidth=1, label= "Linear Regression of Oscillation Maxima")
        ax11.plot(t_o, y, "o", color="darkorange", label="Oscillaltion Maxima", markersize = 5)
        ax11.plot(t_o[0], y[0], "o", color="green", label="Oscillaltion Maximum", markersize = 5)
        ax11.xaxis.set_major_locator(MultipleLocator(0.005))
        ax11.xaxis.set_minor_locator(MultipleLocator(0.001))
        ax11.yaxis.set_major_locator(MultipleLocator(0.5))
        ax11.yaxis.set_minor_locator(MultipleLocator(0.1))
        ax11.set_xlabel("Time [s]")
        ax11.set_ylabel("ln(y)")
        ax11.legend(loc=0, prop={'size': 10})
        #plt.close(fig1)

        ## Defining the exponential line of best fit, with equation y = A0*e^(slope*time)
        ## A0 should equal the oscilation maximum in ideal case
        slope, intercept, r_value_of_lin_reg, p_value_of_lin_reg, std_err = scipy.stats.mstats.linregress(t_o, y)
        A0 = np.exp(intercept)
        t_o = np.array(t_o)
        y_final = function(max(o), slope, t_o)

        ## % Residual Error of Oscialtion Points from Lien of best fit
        res_err_curve = av_abs_residual_error(len(o), y_final, o)
        per_res_error_curve = (res_err_curve / abs(Average(o))) * 100

        frequency,intesnity = Frequency_Analyis(oscilaion_time,oscilation)
        int1, fq1, int2, fq2, int3, fq3, int4, fq4 = top_Freqency_Intensiry(frequency,intesnity)

        ## Main Figure
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches(12, 7)
        fig.suptitle(x.split("/")[-1])
        name, lable_t2, lable_p = Name_lable(x)

        ## define max and min of peizo and the cut away everything before the max
        ax1.axhline(y=0, color="r", linewidth=1)
        #ax1.plot(t, p, color="k", linewidth=1, label=name + " th=" + lable_t2 + " " + lable_p)
        #ax1.plot(t, p, color="k", linewidth=1, label="Filtered Piezo Cut_Out")
        ax1.plot(oscilaion_time, oscilation, color="k", linewidth=1, label="Final Piezo Signal")
        ax1.plot(t_o, y_final, color="dodgerblue", linewidth=1, label="Exponential Line of Best Fit")
        ax1.plot(t_o, o, "o", color="darkorange", label="Oscillation Maxima")
        ax1.plot(t_o[0], o[0], "o", color="green", label="Oscillation Maximum")
        ax1.set_title('(A)')
        ax1.plot(ti_max, pi_max, "o", color="r", label = "Maximum/Minimum of\n Orignial Piezo Signal")
        ax1.plot(ti_min, pi_min, "o", color="r")
        ax1.xaxis.set_major_locator(MultipleLocator(0.05))
        ax1.xaxis.set_minor_locator(MultipleLocator(0.01))
        ax1.yaxis.set_major_locator(MultipleLocator(0.005))
        ax1.yaxis.set_minor_locator(MultipleLocator(0.001))
        ax1.set_xlabel("Time [s]")
        ax1.set_ylabel("Voltage Output [v]")
        ax1.legend(loc=0, prop={'size': 10})
        ax1.set_xlim(-0.002, 0.04)
        #ax1.set_xlim(-61.815, -61.777)

        ax2.plot(frequency, intesnity, color="dodgerblue", linewidth=1, label="Final Frequency")
        ax2.plot(fq1,int1,"o", color="r")
        ax2.plot(fq2,int2,"o", color="r")
        ax2.plot(fq3,int3,"o", color="r")
        ax2.plot(fq4,int4,"o", color="r")
        ax2.yaxis.set_major_locator(MultipleLocator(0.1))
        ax2.yaxis.set_minor_locator(MultipleLocator(0.05))
        ax2.xaxis.set_major_locator(MultipleLocator(500))
        ax2.xaxis.set_minor_locator(MultipleLocator(100))
        ax2.set_xlabel("Frequency [Hz]")
        ax2.set_ylabel("Intensity a.u.")
        ax2.legend(loc=0, prop={'size': 10})
        ax2.set_ylim(0, 1)
        ax2.set_title('(B)')


        table_line = []
        table_line.append(x.split("/")[-1])
        table_line.append(per_res_error_curve)
        table_line.append(pi_max)
        table_line.append(0)
        table_line.append(pi_min)
        table_line.append(0)
        table_line.append(o[0])
        table_line.append(0)
        table_line.append(A0)
        table_line.append(0)
        table_line.append(slope)
        table_line.append(0)
        table_line.append(fq1)
        table_line.append(int1)
        table_line.append(fq2)
        table_line.append(int2)
        table_line.append(fq3)
        table_line.append(int3)
        table_line.append(fq4)
        table_line.append(int4)
        table_line.append(0)

        table_line = ','.join(str(x) for x in table_line)
        print(table_line)
        text_file = open("../PIEZO Oscilation Analysis.csv", "a")
        text_file.write(table_line + "\n")
        text_file.close()

    plt.show()

main_raw()
