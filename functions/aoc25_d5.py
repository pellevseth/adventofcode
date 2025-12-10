# -*- coding: utf-8 -*-

"""

"""

import logging
from math import floor

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

def main(*args, **kwargs):
    fp = 'data/raw/aoc_2025_day5.txt'
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
    answer_part_two, ranges = part_two(ranges)

    logger.info('Part two found {} IDs'.format(answer_part_two))
    df = pd.DataFrame(ranges)
    with open('data/processed/aoc_2025_d5_res.csv', 'w') as ofile:
        df.to_csv(ofile, index=False)
    logger.info('Finished')


def calculate_overlap(row):

    if row['start_next'] > row['stop']:
        return 0
    else:
        return row['stop'] - row['start_next'] + 1

def part_two(ranges):

    ranges = np.sort(ranges, axis=1)

    # Looping until we have no more to combine
    n_merges = 0
    data = list()
    offset = 0
    while True:

        new = list()

        # If we have a odd number we offset by 1
        if len(ranges) % 2 != 0:
            offset = 1
            new.append(ranges[0])
        else:
            offset = 0

        N_pairs = floor(len(ranges) / 2)
        for i in range(N_pairs):

            r0 = ranges[2 * i + offset]
            r1 = ranges[2 * i + 1 + offset]

            if r1[0] <= r0[1]:
                new.append((min(r0[0], r1[0]),
                            max(r1[1], r1[1])))
                n_merges = n_merges + 1
            else:
                new.append(r0)
                new.append(r1)

        data.append({'len_r3': len(ranges), 'N_merges': n_merges})

        if n_merges == 0:
            break
        n_merges = 0
        ranges = new

    return sum([end - start + 1 for start, end in ranges]), ranges


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
