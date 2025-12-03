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
    # dial = np.arange(low, high + 1)

    pos = 50

    pattern = '(?P<direction>[LR]{1})(?P<distance>[0-9]*)'
    p = re.compile(pattern)

    count = 0
    count_pass = 0

    data = list()

    for rotation in inputdata:
        m = p.search(rotation)

        # Check pos before rotating
        pos0 = pos

        # Parse rotation
        direction = 1 if m.group('direction') == 'R' else -1
        distance = int(m.group('distance'))

        # How many rounds are we rotating
        n_rounds = floor(distance / span)

        # Rest
        rest = distance - n_rounds * span

        placements = [pos0 for n in range(0, n_rounds + 1)]
        pos = pos0 + direction * rest

        if low <= pos <= high:
            pass
        elif pos == high + 1:
            pos = low
        elif pos < low:
            pos = pos + span
            if pos0 != low:
                count_pass = count_pass + 1
        elif pos > high:
            pos = pos - span
            count_pass = count_pass + 1

        placements.append(pos)
        logger.info(','.join(map(str, placements)))

        count_pass = count_pass + n_rounds
        if placements[-1] == low:
            count = count + 1

        logger.info(f'rot: {rotation} pos0: {pos0} pos:{pos} count:{count} count_pass:{count_pass}')
        data.append({'rot': rotation, 'pos0': pos0, 'pos': pos, 'distance': distance,
                     'count': count, 'count_pass': count_pass})

    df = pd.DataFrame(data)
    df['passes'] = df['count_pass'] - df['count_pass'].shift(1)
    logger.info(f'Finished, found {count} zeros')
    logger.info(f'Finished, passed zero {count_pass} times')
    logger.info(f'New password {count + count_pass}')

    logger.info('Finished')


def read_input(fp):
    with open(fp, 'r') as ifile:
        lines = ifile.readlines()
    return lines
