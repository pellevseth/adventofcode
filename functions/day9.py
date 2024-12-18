# -*- coding: utf-8 -*-

"""

"""

import logging

import numpy as np
import pandas as pd

from grid.BaseGrid import read_grid

logger = logging.getLogger(__name__)

def main(*args, **kwargs):

    fp = 'data/raw/aoc_2024_day9.txt'

    example = '2333133121414131402'
    #data = example
    data = read_input(fp)

    logger.info('Reading')
    file_id = 0
    s = list()
    for i in range(round(len(data) / 2)):
        
        s1 = [file_id for ii in range(int(data[2 * i]))]
        s.extend(s1)
        file_id = file_id + 1

        try:
            s2 = ['.' for ii in range(int(data[2 * i + 1]))]
            s.extend(s2)
        except IndexError:
            break

    s = np.array(s)
    fp = 'data/intermediate/aoc_2024_day9.txt'
    with open(fp, 'w') as ofile:
        np.savetxt(ofile, s, fmt='%s')
   
    # Start moving

    # Index of empties
    idx_empty = np.where(s == '.')[0]
    idx_int = np.where(s != '.')[0]

    logger.info('Moving')
    N = 1
    while len(idx_int) > 0:

        # Moving        
        s[idx_empty[0]]= s[idx_int[-1]]
        s[idx_int[-1]] = '.'

        if N % 1000 == 0:
            logger.info(N)
        
        N = N + 1
        idx_empty = idx_empty[1:]            
        idx_int = idx_int[:-1]

        if idx_empty.min() >= idx_int.max():
            break
    
    
    print(sum([idx * int(n) for idx, n in enumerate(s) if n != '.']))
    
    fp = 'data/intermediate/aoc_2024_day9_res.txt'
    with open(fp, 'w') as ofile:
        np.savetxt(ofile, s.T, fmt='%s')

def read_input(fp):
    with open(fp, 'r') as ifile:
        lines = ifile.readlines()
    return lines[0]


def find_rightmost_int(s):
    l = len(s)
    for i in range(l):
        try:
            n = int(s[l - i])
        except:
            continue
        break
    return l - i

def find_leftmost_dot(s):
    l = len(s)
    for i in range(l):
        if s[i] == '.':
            break
    return i