"""
file: periodRanking.py
language: python 3
author: Duc Duy Phan - ddp3945@rit.edu
description:
"""

from indexTools import *


def quarter_data(data, year, qtr):
    qd = []
    for region in data:
        entry = data[region]
        for e in entry:
            if e.year == year and e.qtr == qtr:
                qd.append((region, e.index))
    qd.sort(key=lambda e: e[1], reverse=True)
    return qd


def annual_data(data, year):
    ad = []
    for region in data:
        entry = data[region]
        for e in entry:
            if e.year == year:
                ad.append((region, e.index))
    ad.sort(key=lambda e: e[1], reverse=True)
    return ad


def main():
    filepath = input('Enter region-based house price index filename: ')
    filepath = 'data/' + filepath
    year = int(input('Enter year of interest for house prices: '))
    state = False
    ZIP = False
    if filepath.find('state') > -1:
        data = read_state_house_price_data(filepath)
        state = True
    elif filepath.find('ZIP') > -1:
        data = read_zip_house_price_data(filepath)
        ZIP = True

    if state:
        data = annualize(data)
    ad = annual_data(data, year)
    print_ranking(ad, heading='{} Annual Ranking'.format(year))

if __name__ == '__main__':
    main()
