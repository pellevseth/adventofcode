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
    fp = 'data/raw/aoc_2025_day2.txt'

    inputdata = open(fp, 'r').read()

    data = list()

    for r in inputdata.split(','):
        n0, n1 = r.split('-')
        v0 = int(n0)
        v1 = int(n1)

        first_part_prev = None

        while v0 <= v1:
            # Digits in first number
            l0 = len(n0)

            if l0 % 2 == 0:

                # Get the first part
                first_part = n0[0:l0 // 2]
                # We only need to check each first part once
                if first_part_prev == first_part:
                    v0 = v0 + 1
                    n0 = str(v0)
                    continue
                first_part_prev = first_part

                # Make a value to check for
                value = int(f'{first_part}{first_part}')

                if v0 <= value <= v1:
                    data.append({'value': value, 'range': r})

            # Increment
            v0 = v0 + 1
            n0 = str(v0)


    df = pd.DataFrame(data)
    logger.info('The answer is {}'.format(df.value.sum()))
    logger.info('Finished')


def read_input(fp):
    with open(fp, 'r') as ifile:
        lines = ifile.readlines()
    return lines
