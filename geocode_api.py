#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Stefan Jansen'

from io import StringIO
from tempfile import NamedTemporaryFile

import pandas as pd
import requests


class GeoEncoder:
    URL = 'https://geocoding.geo.census.gov/geocoder'
    data_set = 'Public_AR'
    spatial_benchmark = 'current'
    geo_vintage = 'current'
    benchmark = '_'.join([data_set, spatial_benchmark])
    vintage = '_'.join([spatial_benchmark, geo_vintage])

    def __init__(self, data, return_type='geographies', lookup_type='addressbatch'):
        self.return_type = return_type
        self.lookup_type = lookup_type
        self.df = data

    def create_temp_file(self):
        with NamedTemporaryFile(suffix='.csv') as temp:
            self.df.to_csv(temp.name, header=None, index=False)
            return {'addressFile': open(temp.name, 'rb')}

    def get_response(self):
        url = '/'.join([self.URL, self.return_type, self.lookup_type])
        files = self.create_temp_file()
        data = {'benchmark': self.benchmark, 'vintage': self.vintage, 'layers': 'all', 'format': 'jsonp'}
        with requests.Session() as s:
            return s.request(method='POST', url=url, data=data, files=files, verify=False)

    def parse_results(self):
        return_cols = ['addressid', 'address', 'result', 'match_type', 'address_match', 'lat_long',
                       'tiger', 'side', 'state', 'county', 'tract', 'block']
        response = self.get_response()
        try:
            parsed = pd.read_csv(StringIO(response.content.decode('utf-8')), header=None, dtype=str, names=return_cols)
        except UnicodeDecodeError:
            parsed = pd.read_csv(StringIO(response.content.decode('latin1')), header=None, dtype=str, names=return_cols)

        parsed['addressid'] = parsed['addressid'].astype(int)

        if parsed.lat_long.dropna().count() > 0:
            parsed[['lat', 'long']] = parsed.lat_long.str.split(',', expand=True).apply(pd.to_numeric, args=('ignore',))

        return parsed.drop('lat_long', axis=1)

