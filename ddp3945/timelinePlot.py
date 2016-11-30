"""
file: timelinePlot.py
language: python 3
author: Duc Duy Phan - ddp3945@rit.edu
description: Implementation for Task 4 - Project CSCI-141
"""

from indexTools import *
import numpy as np
import numpy.ma as ma
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import copy
import random


def build_plottable_array(xyears, regiondata):
    """
    list(int) * list(AnnualHPI) -> masked NumpyArray
    Build a plottable array from the data provided
    """
    arr = ma.array([0.0 for _ in range(len(xyears))])
    yrs = [e.year for e in regiondata]

    for e in regiondata:
        if e.year in xyears:
            arr[xyears.index(e.year)] = e.index
    for i in range(len(xyears)):
        if not xyears[i] in yrs:
            arr[i] = ma.masked
    return arr


def filter_years(data, year0, year1):
    """
    dict(key=str, value=AnnualHPI) * int * int -> dict(key=str, value=AnnualHPI)
    Pre-condition: year0 <= year1
    """
    filtered_data = dict()
    for region in data:
        filtered_data[region] = [e for e in data[region] if year0 <= e.year <= year1]
        filtered_data[region].sort(key=lambda e: e.year)
    return filtered_data


def plot_HPI(data, regionList):
    """
    dict(key=str, value=AnnualHPI) * list(str) -> NoneType
    Plot the timeline of the data of specified regions in the regionList
    """
    xyears = []
    for region in regionList:
        xyears += [e.year for e in data[region] if not e.year in xyears]
    xyears.sort()
    years = np.array(xyears)

    for region in regionList:
        dataRegion = build_plottable_array(xyears, data[region])
        color = tuple([random.random() for _ in range(3)])
        plt.plot(years, dataRegion, '*', linestyle='-', color=color, label=region)

    plt.title('Home Price Indices: {}-{}'.format(xyears[0], xyears[-1]))
    plt.legend(loc='best')
    plt.xlim(xyears[0], xyears[-1])
    plt.show()


def plot_whiskers(data, regionList):
    """
    dict(key=str, value=AnnualHPI) * list(str) -> NoneType
    Boxplot the data of specified regions in the regionList
    """
    dataSets = []
    for region in regionList:
        dataSets.append([e.index for e in data[region]])
    plt.boxplot(dataSets, meanprops=dict(marker='D'), labels=regionList, showmeans=True)
    plt.title('Home Price Indices Comparision. Median is a line. Mean is a diamond.')
    plt.show()


def main():
    filepath = input('Enter region-based house price index filename: ')
    filepath = 'data/' + filepath
    year0 = int(input('Enter the start year of the range to plot: '))
    year1 = int(input('Enter the end year of the range to plot: '))
    regionList = []
    while True:
        region = input('Enter next region for plots (<ENTER> to stop): ')
        if region == '':
            break
        regionList.append(region)

    if filepath.find('state') > -1:
        data = read_state_house_price_data(filepath)
        for region in regionList:
            print_range(data, region)
        data = annualize(data)
    elif filepath.find('ZIP') > -1:
        data = read_zip_house_price_data(filepath)

    data = filter_years(data, year0, year1)
    plot_HPI(data, regionList)
    plot_whiskers(data, regionList)

if __name__ == '__main__':
    main()
