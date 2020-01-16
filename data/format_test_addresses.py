#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Stefan Jansen'

import json
from pathlib import Path

import numpy as np
import pandas as pd

pd.set_option('display.expand_frame_repr', False)
np.random.seed(42)

ADDRESS_COLS = ['address1', 'city', 'state', 'postalcode']


def json_addresses_to_csv():
    """Convert test addresses provided by
        https://github.com/EthanRBrown/rrad
        from json to csv"""
    with Path('addresses-us-all.json').open() as f:
        json_data = json.load(f)['addresses']

    df = (pd.DataFrame(json_data).rename(columns=str.lower).loc[:, ADDRESS_COLS])
    print(df.info())
    df.to_csv('test_addresses.csv')


if __name__ == '__main__':
    json_addresses_to_csv()
