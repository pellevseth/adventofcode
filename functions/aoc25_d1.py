# -*- coding: utf-8 -*-

"""

"""

import logging
import re
from math import floor

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

def main(*args, **kwargs):
    fp = 'data/raw/aoc_2025_day1.txt'

    inputdata = read_input(fp)

    low = 0
    high = 99
    span = (high - low) + 1
    dial = np.arange(low, high + 1)

    pos = 50

    pattern = '(?P<direction>[LR]{1})(?P<distance>[0-9]*)'
    p = re.compile(pattern)

    count = 0
    count_intermediate = 0
    count_pass = 0

    data = list()

    for rotation in inputdata:
        m = p.search(rotation)

        # Check pos before rotating
        pos0 = pos

        direction = 1 if m.group('direction') == 'R' else -1
        distance = int(m.group('distance'))
        pos = pos + distance * direction

        if pos == high + 1:
            pos = low
        elif low <= pos <= high:
            pass
        else:
            if pos < low:
                d = 1
            elif pos > high:
                d = -1
            while pos < low or pos > high:
                pos = pos + d * span
                if pos < low:
                    d = 1
                elif pos > high:
                    d = -1

                if pos == 0:
                    count_intermediate = count_intermediate + 1
                count_pass = count_pass + 1

            # Correct if we started at zero
            if pos0 == 0:
                count_pass = count_pass - 1

        if dial[pos] == 0:
            count = count + 1

        logger.info(f'rot: {rotation} pos:{pos} count:{count} count_pass:{count_pass}')
        data.append({'rot': rotation, 'pos0': pos0, 'pos': pos, 'distance': distance, 'count': count,
                     'count_intermediate': count_intermediate, 'count_pass': count_pass})

    df = pd.DataFrame(data)
    df['passes'] = df['count_pass'] - df['count_pass'].shift(1)
    logger.info(f'Finished, found {count} zeros')
    logger.info(f'Finished, passed zero {count_pass} times')
    logger.info(f'Finished, intermediate stops {count_intermediate} times')
    logger.info(f'New password {count + count_pass + count_intermediate}')

    logger.info('Finished')


def read_input(fp):
    with open(fp, 'r') as ifile:
        lines = ifile.readlines()
    return lines

def how_many_rounds(distance, span):

    # Antall hele runder
    c = floor(distance / span)

    return c
