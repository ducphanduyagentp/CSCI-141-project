"""
file: volatility.py
language: python 3
author: Duc Duy Phan - ddp3945@rit.edu
description: Implementation for Task 3 - Project CSCI-141
"""

from indexTools import *
from math import sqrt

def average(nums):
    """
    list -> float
    Calculate to average of numbers in the list
    """
    if len(nums) == 0:
        return 0.0

    sum = 0.0
    for n in nums:
        sum += n
    return sum / len(nums)


def deviation_squared(nums, avg):
    """
    list * float -> list
    Calculate the squared deviation of numbers in the list
    """
    return [(avg - n) ** 2 for n in nums]


def measure_volatility(data):
    """
    dict(key=str, value=AnnualHPI) -> list(tuple(str, float))
    Calculate to volatility of the dataset
    """
    volatility = []
    for region in data:
        nums = [e.index for e in data[region]]
        avg = average(nums)
        devsqr = deviation_squared(nums, avg)
        sum = 0.0
        for n in devsqr:
            sum += n
        stdev = sqrt(sum / len(nums))
        volatility.append((region, stdev))
    volatility.sort(key=lambda e: e[1], reverse=True)
    return volatility

def main():
    filepath = input('Enter region-based house price index filename: ')
    filepath = 'data/' + filepath
    region = input('Enter the region of interest: ')
    print()

    if filepath.find('state') > -1:
        data = read_state_house_price_data(filepath)
        data = annualize(data)
    elif filepath.find('ZIP') > -1:
        data = read_zip_house_price_data(filepath)

    volatilities = measure_volatility(data)
    print_ranking(volatilities, heading='Annualized Price Standard Deviation, High to Low')
    print()
    print('Note: Absence of data can increase the apparent variation.')
    for e in volatilities:
        if e[0] == region:
            print('Standard deviation for {} is {}'.format(e[0], e[1]))
            return
    print('Region {} not found.'.format(region))


if __name__ == '__main__':
    main()
