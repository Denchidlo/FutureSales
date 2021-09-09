from statsmodels.tsa.stattools import acf 
import numpy as np
import pandas as pd

FUNC_MAP = {}

def _register_as_transformer(func):
    if FUNC_MAP.get(func.__name__, None) is None:
        FUNC_MAP[func.__name__] = func
        return func
    else:
        raise KeyError(f'Unable to register {repr(func)}. Name is already used')
 
def make_transformer(func, **kwargs):
    def wrapped(*frames):
        return func(*frames, **kwargs)
    return wrapped

def extract_id_sequences(df, index=None, seq_index=None, target=None, aggregator=None, fill_na=np.NaN):
    return (
        df.groupby(index + seq_index)[target]
        .apply(aggregator)
        .reset_index()
        .pivot(
            index=index, 
            columns=seq_index, 
            values=target
            )
        .fillna(fill_na))

def diff(series, order, period=1):
    diff_1 = (series - series.shift(period, axis=1))
    if order == 1:
        return diff_1.fillna(0)
    elif order == 2:
        return (diff_1 - diff_1.shift(period, axis=1)).fillna(0)
    else:
        raise ValueError(f'Order higher than 2 is currently unsupported')

def subset2subset(df, series_transformer, column_names, axis=1):
    return df.apply(
        lambda _series: pd.Series(
            series_transformer(_series), 
            index=column_names), 
        axis=1, 
        result_type='expand')

def take_acf(series, nlags):    
    return acf(series, nlags=nlags)[1:]


def append_columns(dataset, columns, transformers):
    for column, transformer in zip(columns, transformers):
        dataset[column] = transformer(dataset)