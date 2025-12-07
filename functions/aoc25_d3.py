# -*- coding: utf-8 -*-

"""

"""

import logging
import re
from copy import deepcopy

import pandas as pd

logger = logging.getLogger(__name__)

def main(*args, **kwargs):
    fp = 'data/raw/aoc_2025_day3_example.txt'
    inputdata = read_input(fp)

    ret = [parse_joltstring_extended(j, 12) for j in inputdata]
    df = pd.DataFrame(data=list(zip(inputdata, ret)), columns=['joltage', 'voltage'])
    logger.info('Answer is {}'.format(df.voltage.sum()))

    logger.info('Finished')

def parse_joltstring(s):
    val = 99

    while val >= 0:
        val_string = str(val)
        pattern = '[0-9]*'.join(['([{0}]{{1}})'.format(x) for x in val_string])
        if re.search(pattern, s):
            return val

        val = val - 1

    return val

def parse_joltstring_extended(s, N):
    """
    s - string to parse
    N - number length of sub-string
    """

    len_s = len(s)

    # Holder track på hvor langt i s man ha kommet
    sub_string = ''

    s2 = deepcopy(s)
    len_s2 = len(s2)

    # Plassering i den nye strengen vår
    for n in range(N):


        # Sjekker ulike første siffer
        for n0 in map(str, list(reversed(range(10)))):
            idx = s2.find(n0)
            n_a = 2
            if (idx > 0) and (n + len_s2 - idx - 1 == N):
                s2 = s2[idx+1:]
                len_s2 = len(s2)
                sub_string = sub_string + n0
                break

    return sub_string

def read_input(fp):
    with open(fp, 'r') as ifile:
        lines = [l.replace('\n', '') for l in ifile.readlines()]
    return lines
