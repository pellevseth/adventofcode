# -*- coding: utf-8 -*-

"""

"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

def main(*args, **kwargs):
    fp = 'data/raw/aoc_2025_day5_example.txt'
    ranges, ingredients = read_input(fp)

    # Make array of the ranges, flatten so we can use searchsorted
    ranges = np.sort(np.array([r.split('-') for r in ranges], dtype=np.int64), axis=0)
    r2 = ranges.flatten()

    # Array of ingredients
    ingredients = np.sort(ingredients)

    # Searchsorted to get indexes
    idx = np.searchsorted(r2, ingredients)

    # Even numbers are outside the given ranges
    idx = np.where(idx % 2 != 0)[0]

    logger.info('Part one, found {} fresh ingredients'.format(len(idx)))

    # Part two
    df = pd.DataFrame(ranges, columns=['start', 'stop']).sort_values('start')
    df['start_next'] = df.start.shift(-1).astype(np.int64)
    df['count'] = df.stop - df.start + 1
    df['overlap'] = df.apply(lambda r: calculate_overlap(r), axis=1)
    df['count_all'] = df['count'] - df['overlap']

    logger.info('Part two found {} IDs'.format(df.count_all.sum()))
    with open('data/processed/aoc_2025_d5_res.csv', 'w') as ofile:
        df.to_csv(ofile, index=False)
    logger.info('Finished')


def calculate_overlap(row):

    if row['start_next'] > row['stop']:
        return 0
    else:
        return row['stop'] - row['start_next'] + 1

def read_input(fp):
    ranges = list()
    ingredients = list()
    with open(fp, 'r') as ifile:
        for r in ifile.readlines():
            if '-' in r:
                ranges.append(r.strip('\n'))
            else:
                if len(r) > 1:
                    ingredients.append(int(r))
    return ranges, ingredients
