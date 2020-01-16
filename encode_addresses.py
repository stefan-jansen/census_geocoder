#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Stefan Jansen'

import argparse
import warnings
from multiprocessing import Pool
from pathlib import Path
from time import time

import numpy as np
import pandas as pd

from geocode_api import GeoEncoder

BATCH_SIZE = 1000

ADDRESS_ID_COLS = ['addressid', 'address1', 'city', 'state', 'postalcode']
ADDRESS_COLS = ADDRESS_ID_COLS[1:]
RESULT_PATH = Path('encoded')
if not RESULT_PATH.exists():
    RESULT_PATH.mkdir()


def format_time(t):
    m, s = divmod(t, 60)
    h, m = divmod(m, 60)
    return f'{h:0>2.0f}:{m:0>2.0f}:{s:0>2.0f}'


def store_result(args):
    data, i, n, start = args
    if i % 10 == 0:
        now = time()
        elapsed = now - start
        remaining = elapsed / i * ((n / BATCH_SIZE) - i)
        print(f'Done: {i:>5,d} | Elapsed: {format_time(elapsed)} | Remaining: {format_time(remaining)}')
    data.to_csv(RESULT_PATH / 'batch_{}.csv'.format(i), index=False)


def match_addresses(batch, i, n, s):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        encoder = GeoEncoder(batch)
        results = encoder.parse_results()
    return batch.merge(results, on='addressid', how='left', suffixes=('', '_id')), i, n, s


def load_addresses(file_name='addresses'):
    try:
        data = pd.read_csv(f'data/{file_name}.csv')
    except FileNotFoundError:
        print(f'File {file_name}.csv does not exist')
        exit()
    if 'addressid' not in data.columns:
        data = data.assign(addressid=list(range(len(data))))
    data.postalcode = data.postalcode.astype(int)
    if len(data.columns.intersection(pd.Index(ADDRESS_ID_COLS))) != 5:
        print('Address file should contain the columns')
        print('address1, city, state, postalcode')
        print('and (optionally) a unique field addressid')
    return data.loc[:, ADDRESS_ID_COLS]


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file_name',
                    default='addresses',
                    help='Address file name (location: data folder)')
args = parser.parse_args()

file_name = args.file_name
data = load_addresses(file_name=file_name)
# print(data.info())
n = len(data)
start = time()
print(f'To do: {data.shape[0]:,d}')

with Pool() as pool:
    results = []
    for i, (_, df) in enumerate(data.groupby(np.arange(n) // BATCH_SIZE), 1):
        r = pool.apply_async(match_addresses, (df, i, n, start), callback=store_result)
        results.append(r)

    for r in results:
        r.wait()

print('Finished in', format_time(time() - start))
