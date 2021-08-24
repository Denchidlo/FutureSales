import numpy as np
import pandas as pd




class SubseriesCreator:
    def __init__(self, df):
        self._context = {
            'dataset': df,
            'transformers': {}
        }

    def get_series(self, key):
        if key in self._context['transformed']:
            return self._context['transformed'][key]
        else:
            return self._context['dataset'][key]

    def _serieses2series(self, name, func, affected_names):
        affected_serieses = [
            self.get_series(_name) for _name in affected_names
        ]

        self._context['transformed'][name] = func(affected_serieses)

        return self._context['transformed'][name]

    def _dataframe2series(self, name, func):
        self._context['transformed'][name] = func(self._context['dataset'])

        return self._context['transformed'][name]


def make_transformer(func, **kwargs):

    def wrapped(serieses):
        return func(serieses, **kwargs)
    
    return wrapped

def lag(series, period=None, fill_na=None):
    return series.shift(period).fillna(fill_na)

def diff(series, order, period=1):
    diff_1 = (series - series.shift(period))
    if order == 1:
        return diff_1.fillna(0)
    elif order == 2:
        return (diff_1 - diff_1.shift(period)).fillna(0)
    else:
        raise ValueError(f'Order higher than 2 is currently unsupported')

def aggregate(df, group, target, func):
    return df.groupby(group)[target].agg(func)

def create_name_transformer(force_category, pattern):
    def _wrapped(value):
        if value in force_category:
            return force_category[value]

        split = value.split(pattern)
        if len(split) > 1:
            return split[0]

        return value
    return _wrapped

def append_columns(dataset, columns, transformers):
    for column, transformer in zip(columns, transformers):
        dataset[column] = transformer(dataset)