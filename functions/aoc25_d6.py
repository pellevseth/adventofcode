# -*- coding: utf-8 -*-

"""

"""

import logging
from math import prod

import numpy as np

logger = logging.getLogger(__name__)

def main(*args, **kwargs):
    fp = 'data/raw/aoc_2025_day6.txt'

    values, operators = read_input_simple(fp)
    answer_part_one = part_one(np.array(values, dtype=np.int64), operators)
    logger.info('Part one, answer is {}'.format(answer_part_one))

    # Part two
    data = read_input(fp)
    answer_part_two = part_two(data)

    logger.info('Part two answer is {}'.format(answer_part_two))
    logger.info('Finished')

def parse_operator(s):
    if s == '+':
        return sum
    elif s == '*':
        return prod

def part_one(values, operators):

    res = list()
    for idx, op in enumerate(operators):
        res.append(parse_operator(op)(values[:,idx]))
    return sum(res)

def part_two(data):
    a = np.array(data)
    values = a[:,:-1,:]
    operators = a[:,-1,:]

    res = list()
    for idx, op in enumerate(operators):
        a2 = values[idx]
        v = [int(''.join(a2[:,c])) for c in range(a2.shape[0])]
        res.append(parse_operator(op[0])(v))

    return sum(res)


def read_input_simple(fp):
    with open(fp, 'r') as ifile:
        lines = [l.replace('\n', '').split() for l in ifile.readlines()]
    return lines[:-1], lines[-1]

def read_input(fp):

    with open(fp, 'r') as ifile:
        lines = [l.replace('\n', '') for l in ifile.readlines()]

    data = list()
    part = [list() for l in lines]

    n_col = 0
    idx = 0
    n_parts = len(lines[-1].split())
    while True:

        column = list()
        for l in lines:
            try:
                v = l[n_col]
            except:
                v = ' '
            column.append(v)
        n_col = n_col + 1

        if list(set(column))[0] == ' ' and len(list(set(column))) == 1:
            data.append(part)
            part = [list() for l in lines]
            idx = idx + 1

            if idx >= n_parts:
                break

            continue

        for row, col in zip(part, column):
            row.append(col)

    return data
