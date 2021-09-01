import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf 

def make_transformer(func, **kwargs):
    def wrapped(serieses):
        return func(serieses, **kwargs)
    return wrapped

# Applied funcs
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


def take_subseries(df, columns, new_name):
    if isinstance(columns, list): 
        return df.loc[:, columns].rename(dict([zip(columns, new_name)]))
    else:
        return df.loc[:, df.columns[columns]].rename(dict(zip(df.columns[columns], new_name)), axis=1)

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


FUNC_MAP = {

}