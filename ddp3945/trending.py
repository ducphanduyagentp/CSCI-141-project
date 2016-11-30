"""
file: trending.py
language: python 3
author: Duc Duy Phan - ddp3945@rit.edu
description: Implementation for Task 2 - Project CSCI-141
"""
from indexTools import *

def cagr(idxlist, periods):
    """
    list(float) * int -> float
    Calculate Compound Annual Growth Rate for given data
    """
    return ((idxlist[-1]/idxlist[0]) ** (1/periods) - 1) * 100


def calculate_trends(data, year0, year1):
    """
    dict(key=str, value=AnnualHPI) * int * int -> list(tuple(str, float))
    Calculate the year-to-year rate of change of the dataset
    Pre-condition: year0 < year1
    """
    trend = []
    for region in data:
        entry = data[region]
        idxlist = []
        for e in entry:
            if e.year == year1:
                idxlist.append(e.index)
            elif e.year == year0:
                idxlist.insert(0, e.index)
        if len(idxlist) < 2:
            continue
        trend.append((region, cagr(idxlist, year1 - year0)))
    trend.sort(key=lambda e: e[1], reverse=True)
    return trend


def main():
    filepath = input('Enter region-based house price index filename: ')
    filepath = 'data/' + filepath
    year0 = int(input('Enter start year of interest: '))
    year1 = int(input('Enter ending year of interest: '))
    print()

    if filepath.find('state') > -1:
        data = read_state_house_price_data(filepath)
        data = annualize(data)
    elif filepath.find('ZIP') > -1:
        data = read_zip_house_price_data(filepath)


    trend = calculate_trends(data, year0, year1)
    print_ranking(trend, heading='{}-{} Compound Annual Growth Rate'.format(year0, year1))


if __name__ == '__main__':
    main()
