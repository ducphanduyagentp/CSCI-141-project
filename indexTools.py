"""
file: indexTools.py
language: python 3
author: Duc Duy Phan - ddp3945@rit.edu
description:
"""
from rit_lib import *


class QuarterHPI(struct):
    _slots = ((int, 'year'), (int, 'qtr'), (float, 'index'))


class AnnualHPI(struct):
    _slots = ((int, 'year'), (float, 'index'))


def read_state_house_price_data(filepath):
    """str -> dict"""
    warningMsg = "data unavailable:"
    data = dict()
    for line in open(filepath):
        if line[:5] == 'state':
            continue
        missingData = False
        entry = line.split()
        for i in range(4):
            e = entry[i]
            if e == '.':
                missingData = True
                print(warningMsg)
                print(line)
                break
        if not missingData:
            key = entry[0]
            quarterHPI = QuarterHPI(
                int(entry[1]), int(entry[2]), float(entry[3]))
            if key in data:
                data[key].append(quarterHPI)
            else:
                data[key] = [quarterHPI]
    return data


def read_zip_house_price_data(filepath):
    """str -> dict"""
    data = dict()
    total = 0
    count = 0
    for line in open(filepath):
        if not line[0].isdigit():
            continue
        total += 1
        missingData = False
        entry = line.split()
        for i in [0, 1, 3]:
            e = entry[i]
            if e == '.':
                missingData = True
                break
        if not missingData:
            count += 1
            key = entry[0]
            annualHPI = AnnualHPI(int(entry[1]), float(entry[3]))
            if key in data:
                data[key].append(annualHPI)
            else:
                data[key] = [annualHPI]
    print('count: {} uncounted: {}'.format(count, total - count))
    return data


def index_range(data, region):
    """dict * str -> tuple"""
    dataRange = data[region]
    dataRange.sort(key=lambda e: e.index)
    return (dataRange[0], dataRange[-1])


def print_range(data, region):
    low, high = index_range(data, region)
    print("Region: {}".format(region))
    if isinstance(low, QuarterHPI):
        print("Low: year/quarter/index: {} / {} / {}".format(low.year, low.qtr, low.index))
        print("High: year/quarter/index: {} / {} / {}".format(high.year,
                                                              high.qtr, high.index))
    elif isinstance(low, AnnualHPI):
        print("Low: year/index: {} / {}".format(low.year, low.index))
        print("High: year/index: {} / {}".format(high.year, high.index))


def print_ranking(data, heading="Ranking"):
    print(heading)
    print('The Top 10:')
    for i in range(10):
        print('{} : {}'.format(i + 1, data[i]))
    print('The Bottom 10:')
    for i in range(len(data) - 10, len(data)):
        print('{} : {}'.format(i + 1, data[i]))


def annualize(data):
    data_annual = dict()
    for region in data:
        entry = data[region]
        d = dict()
        for e in entry:
            yr = e.year
            if not yr in d:
                d[yr] = (e.index, 1)
            else:
                d[yr] = (d[yr][0] + e.index, d[yr][1] + 1)
        for yr in d:
            newIndex = d[yr][0] / d[yr][1]
            annualHPI = AnnualHPI(yr, newIndex)
            if not region in data_annual:
                data_annual[region] = [annualHPI]
            else:
                data_annual[region].append(annualHPI)
    return data_annual


def main():
    filepath = input('Enter house price index file: ')
    filepath = 'data/' + filepath
    state = False
    ZIP = False
    if filepath.find('state') > -1:
        data = read_state_house_price_data(filepath)
        state = True
    elif filepath.find('ZIP') > -1:
        data = read_zip_house_price_data(filepath)
        ZIP = True

    regions = []
    while True:
        region = input('Next region of interest( Hit ENTER to stop): ')
        if region == '':
            break
        regions.append(region)
    print('=' * 70)
    for region in regions:
        if state:
            print_range(data, region)
            annual = annualize(data)
            print_range(annual, region)
            print('Annualized Index Values for {}'.format(region))
            annual[region].sort(key=lambda c: c.year)
            for e in annual[region]:
                print(e)
        elif ZIP:
            print_range(data, region)
            data[region].sort(key=lambda c: c.year)
            for e in data[region]:
                print(e)


if __name__ == '__main__':
    main()
