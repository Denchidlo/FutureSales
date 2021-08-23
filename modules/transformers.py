import numpy as np
import pandas as pd




class Transformer:
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

    def create_series(self, name, func, affected_names):
        affected_serieses = [
            self.get_series(_name) for _name in affected_names
        ]

        self._context['transformed'][name] = func(*affected_serieses)

        return self._context['transformed'][name]


def make_transformer(func, **kwargs):

    def wrapped(*serieses):
        return func(*serieses, **kwargs)
    
    return wrapped

def lag(series, period=None, fill_na=None):
    return series.shift(period).fillna(fill_na)

def diff(series, order):
    if order == 1:
        return (series - series.shift(1)).fillna(0)