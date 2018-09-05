#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2018 Embest
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sqlite3
import os
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import MinuteLocator, HourLocator, DateFormatter

import matplotlib.dates as mdates
import time

CONSTELLATION = {1:"GP",2:"GL",3:"QZ",4:"BD",5:"GA",6:"NC"}

def plotSnr(database,constellations,top=4):
    GPSL1Time = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28:[], 29:[], 30:[], 31:[], 32:[] }
    GPSL1Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28:[], 29:[], 30:[], 31:[], 32:[] }
    
    GLOL1Time = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[]}
    GLOL1Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[]}
    
    QZSL1Time = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[] }
    QZSL1Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[] }

    BDSL1Time = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28:[], 29:[], 30:[], 31:[], 32:[], 33:[], 34:[], 35:[], 36:[], 37:[], 38:[], 39:[]}
    BDSL1Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28:[], 29:[], 30:[], 31:[], 32:[], 33:[], 34:[], 35:[], 36:[], 37:[], 38:[], 39:[]}

    GALL1Time = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28:[], 29:[], 30:[], 31:[], 32:[], 33:[], 34:[], 35:[], 36:[], 37:[], 38:[], 39:[]}
    GALL1Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28:[], 29:[], 30:[], 31:[], 32:[], 33:[], 34:[], 35:[], 36:[], 37:[], 38:[], 39:[]}

    GPSL5Time = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28:[], 29:[], 30:[], 31:[], 32:[] }
    GPSL5Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28:[], 29:[], 30:[], 31:[], 32:[] }
    
    GLOL5Time = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[]}
    GLOL5Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[]}
    
    QZSL5Time = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[] }
    QZSL5Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[] }

    BDSL5Time = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28:[], 29:[], 30:[], 31:[], 32:[], 33:[], 34:[], 35:[], 36:[], 37:[], 38:[], 39:[]}
    BDSL5Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28:[], 29:[], 30:[], 31:[], 32:[], 33:[], 34:[], 35:[], 36:[], 37:[], 38:[], 39:[]}

    GALL5Time = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28:[], 29:[], 30:[], 31:[], 32:[], 33:[], 34:[], 35:[], 36:[], 37:[], 38:[], 39:[]}
    GALL5Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[], 19:[], 20:[], 21:[], 22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28:[], 29:[], 30:[], 31:[], 32:[], 33:[], 34:[], 35:[], 36:[], 37:[], 38:[], 39:[]}

    IRNL1Time = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[]}
    IRNL1Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[]}
    
    TopL5Time = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[] }
    TopL5Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[] }

    TopL1Time = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[] }
    TopL1Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[] }

    UtcTime = 0

    L5Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[] }
    L1Snr  = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[] }

    count = 0
    conn = sqlite3.connect(database)
    c = conn.cursor()
    for row in c.execute('SELECT * FROM GSV ORDER BY Time'):
        if row[0] > 1000000000:
            time = datetime.utcfromtimestamp(row[0])
            if row[3]==1 and row[2] and row[3] in constellations and row[6]==0:
                GPSL1Time[row[1]].append(time)
                GPSL1Snr[row[1]].append(row[2])
                L1Snr[row[3]].append(row[2])
            elif row[3] == 2 and row[2] and row[3] in constellations and row[6]==0:
                GLOL1Time[row[1]-64].append(time)
                GLOL1Snr[row[1]-64].append(row[2])
                L1Snr[row[3]].append(row[2])
            elif row[3] == 3 and row[2] and row[3] in constellations and row[6]==0:
                QZSL1Time[row[1]].append(time)
                QZSL1Snr[row[1]].append(row[2])
                L1Snr[row[3]].append(row[2])
            elif row[3] == 4 and row[2] and row[3] in constellations and row[6]==0:
                BDSL1Time[row[1]-200].append(time)
                BDSL1Snr[row[1]-200].append(row[2])
                L1Snr[row[3]].append(row[2])
            elif row[3] == 5 and row[2] and row[3] in constellations and row[6]==0:
                GALL1Time[row[1]-100].append(time)
                GALL1Snr[row[1]-100].append(row[2])
                L1Snr[row[3]].append(row[2])
            elif row[3] == 6 and row[2] and row[3] in constellations and row[6]==0:
                IRNL1Time[row[1]].append(time)
                IRNL1Snr[row[1]].append(row[2])
                L1Snr[row[3]].append(row[2])
            elif row[3]==1 and row[2] and row[3] in constellations and row[6]==8:
                GPSL5Time[row[1]].append(time)
                GPSL5Snr[row[1]].append(row[2])
                L5Snr[row[3]].append(row[2])
            elif row[3] == 3 and row[2] and row[3] in constellations and row[6]==8:
                QZSL5Time[row[1]].append(time)
                QZSL5Snr[row[1]].append(row[2])
                L5Snr[row[3]].append(row[2])
            elif row[3] == 5 and row[2] and row[3] in constellations and row[6]==1:
                GALL5Time[row[1]-100].append(time)
                GALL5Snr[row[1]-100].append(row[2])
                L5Snr[row[3]].append(row[2])

            if UtcTime!=row[0]:
                print(UtcTime)
                for i in constellations:
                    if len(L1Snr[i]) >= top:
                        L1Snr[i].sort(reverse=True)
                        avg = sum(L1Snr[i][0:top])/top
                        TopL1Time[i].append(time)
                        TopL1Snr[i].append(avg)
                        print(UtcTime, "L1", avg)
                    if len(L5Snr[i]) >= top:
                        L5Snr[i].sort(reverse=True)
                        avg = sum(L5Snr[i][0:top])/top
                        TopL5Time[i].append(time)
                        TopL5Snr[i].append(avg)
                        print(UtcTime, "L5", avg)
                
                UtcTime = row[0]
                count+=1
                for i in constellations:
                    L1Snr[i] = []
                    L5Snr[i] = []

    fig, ax = plt.subplots()

    for key in GPSL1Time.keys():
        if len(GPSL1Time.get(key)) > 0:
            lab = "GP"+str(key)
            ax.plot(GPSL1Time[key], GPSL1Snr[key], linestyle='-', marker='v', linewidth=1.5,  label=lab)

    for key in GLOL1Time.keys():
        if len(GLOL1Time.get(key)) > 0:
            lab = "GL"+str(key)
            ax.plot(GLOL1Time[key], GLOL1Snr[key], linestyle='-', marker='o', linewidth=1.5,  label=lab)

    for key in QZSL1Time.keys():
        if len(QZSL1Time.get(key)) > 0:
            lab = "QZ"+str(key)
            plt.plot(QZSL1Time[key], QZSL1Snr[key], linestyle='-', marker='1', linewidth=1.5,  label=lab)

    for key in BDSL1Time.keys():
        if len(BDSL1Time.get(key)) > 0:
            lab = "BD"+str(key)
            plt.plot(BDSL1Time[key], BDSL1Snr[key], linestyle='-', marker='x', linewidth=1.5,  label=lab)

    for key in GALL1Time.keys():
        if len(GALL1Time.get(key)) > 0:
            lab = "GA"+str(key)
            plt.plot(GALL1Time[key], GALL1Snr[key], linestyle='-', marker='*', linewidth=1.5,  label=lab)

    for key in GPSL5Time.keys():
        if len(GPSL5Time.get(key)) > 0:
            lab = "GP"+str(key)
            ax.plot(GPSL5Time[key], GPSL5Snr[key], linestyle='-.', marker='^', linewidth=1.5,  label=lab)

    for key in QZSL5Time.keys():
        if len(QZSL5Time.get(key)) > 0:
            lab = "QZ"+str(key)
            plt.plot(QZSL5Time[key], QZSL5Snr[key], linestyle='-.', marker='2', linewidth=1.5,  label=lab)

    for key in GALL5Time.keys():
        if len(GALL5Time.get(key)) > 0:
            lab = "GA"+str(key)
            plt.plot(GALL5Time[key], GALL5Snr[key], linestyle='-.', marker='+', linewidth=1.5,  label=lab)

    for key in IRNL1Time.keys():
        if len(IRNL1Time.get(key)) > 0:
            lab = "NC"+str(key)
            plt.plot(IRNL1Time[key], IRNL1Snr[key], linestyle='-', marker='+', linewidth=1.5,  label=lab)

    textstr = ""
    for key in TopL1Time.keys():
        if len(TopL1Time.get(key)) > 0:
            lab = CONSTELLATION[key]+ "T"+str(top)
            plt.plot(TopL1Time[key], TopL1Snr[key], linestyle='-', marker='+', linewidth=5,  label=lab)
            textstr += CONSTELLATION[key] + " L1 Top" + str(top) + " Avg: " + '{:4.2f}'.format(sum(TopL1Snr[key])/len(TopL1Snr[key])) + " In:" + str(len(TopL1Snr[key])) + "\n"

    for key in TopL5Time.keys():
        if len(TopL5Time.get(key)) > 0:
            lab = CONSTELLATION[key]+ "T"+str(top)+"L5"
            plt.plot(TopL5Time[key], TopL5Snr[key], linestyle='-', marker='+', linewidth=5,  label=lab)
            textstr += CONSTELLATION[key] + " L5 Top" + str(top) + " Avg: " + '{:4.2f}'.format(sum(TopL5Snr[key])/len(TopL5Snr[key])) + " In:" + str(len(TopL5Snr[key])) + "\n"

    ax.grid(True, linestyle='-.')

    locator = 0
    if count < 1000:
        locator = 1
    elif count < 2000:
        locator = 2
    else:
        locator = 4
    

    ax.xaxis.set_major_locator(MinuteLocator(range(0, 60, locator)))
    # ax.xaxis.set_minor_locator(MinuteLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%H%M%S'))

    ax.format_xdata = mdates.DateFormatter('%H%M%S')
    
    plt.legend(loc='upper right')

    plt.ylabel("dBHz")
    plt.xlabel("UTC")
    plt.title('SNR')

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)

    plt.xticks(rotation=90)

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, textstr.strip(), transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

    plt.show()


def plotSpeed(database):
    Time = []
    Speed  = []

    conn = sqlite3.connect(database)
    c = conn.cursor()
    for row in c.execute('SELECT * FROM RMC ORDER BY Time'):
        if row[0] > 1000000000:
            time = datetime.utcfromtimestamp(row[0])
            Time.append(time)
            Speed.append(row[4])
            
    fig, ax = plt.subplots()


    lab = "Speed"
    ax.plot(Time, Speed, linestyle='-', marker='v', linewidth=1.5,  label=lab)

    ax.grid(True, linestyle='-.')

    ax.xaxis.set_major_locator(MinuteLocator(range(0, 60, 4)))
    ax.xaxis.set_minor_locator(MinuteLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%H%M%S'))

    ax.format_xdata = mdates.DateFormatter('%H%M%S')
    
    plt.legend()

    plt.ylabel("Knot")
    plt.xlabel("UTC")
    plt.title('SPEED')

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)

    plt.xticks(rotation=90)

    plt.show()


def main():
    parser = argparse.ArgumentParser(description='NMEA Analyzer Plot Tool', 
                                     epilog='Example>> nmeaplot gps.nmea.db')
    parser.add_argument('input',  type=str , help= "input file: db file")
    parser.add_argument('option', type=str , help= "option: snr, speed")
    parser.add_argument('-c',     type=int, default= 0, help='Constellations, default is 0')
    parser.add_argument('-t',     type=int, default= 4, help='topN strongest points in summary, default is 4')
    args = parser.parse_args()
    print(args)

    if args.option == 'snr':
        constellations = [0]
        if args.c == 0:
            constellations = [1,2,3,4,5,6]
        else:
            constellations = [args.c]
        print("plot SNR")
        plotSnr(args.input,constellations, args.t)
    elif args.option == 'speed':
        plotSpeed(args.input)
    else:
        print("option not supported")


if __name__ == '__main__':
    main()


