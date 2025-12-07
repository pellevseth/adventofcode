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

        # Sjekker alle sub-strenger for opptil halve lengden av den lengste
        for id in map(str, range(v0, v1+1)):

            len_id = len(id)

            # Ser på lengde av streng
            N = 1

            # Check if we can divide into equal or if length we are checking is more than half the length
            while N <= len_id // 2:
                if len_id % N != 0:
                    N = N + 1
                    continue
                sub_string = id[0:N]
                ret = re.findall(sub_string, id)

                # Add if we found the same number as the number of substrings we are checking
                if sub_string * (len_id // N) == id:
                    data.append({'value': int(id), 'range': r})
                N = N + 1

    df = pd.DataFrame(data)
    logger.info('The answer is {}'.format(df.drop_duplicates().value.sum()))
    logger.info('Finished')


def read_input(fp):
    with open(fp, 'r') as ifile:
        lines = ifile.readlines()
    return lines
