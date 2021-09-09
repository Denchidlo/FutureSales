from .transformers import *

def take_subseries(df, columns, new_name):
    if isinstance(columns, list):
        return df.loc[:, columns].rename(dict(zip(columns, new_name)))
    else:
        return df.loc[:, df.columns[columns]].rename(dict(zip(df.columns[columns], new_name)), axis=1)

def take_percentiles(df, percentiles, idx, month, funcs=[]):
    def __thresh(row, percentile):
        return np.percentile(row, percentile)
    
    def __mean(row, percentile, idx):
        _mean = tr.diff(row[row >=  __thresh(row, percentile)].reset_index(), 1)[idx]
        _responce = _mean[_mean > 1].mean()
        return _responce if _responce is not np.NaN else 999 

    def __last(row, idx, percentile):
        return row[row <= __thresh(row, percentile)].reset_index()[idx].to_list()[-1]

    _data_responce = None
    for percentile in percentiles:
        _thresh = df.apply(make_transformer(__thresh, percentile=percentile), axis=1)
        # print(f'thresh found {_thresh}')
        _mean = df.apply(make_transformer(__mean, percentile=percentile, idx=idx), axis=1)
        # print(f'mean found {_mean}')
        _last = df.apply(make_transformer(__last, percentile=percentile, idx=idx), axis=1)
        # print(f'last found {_last}')
        _percentile_value = _thresh * (1 - np.divide((month - _last), _mean))

        current_percentile = pd.concat([_thresh, _mean, _last, _percentile_value], axis=1)
        current_percentile.columns = [f'percentile_{percentile}_{name}' for name in ['thresh', 'mean', 'last', 'value']]

        if _data_responce is None:
            _data_responce = current_percentile
        else:
            _data_responce = pd.concat([_data_responce, current_percentile])

    return _data_responce

def create_aggregation_pipeline(df, func_queue):
    dataset = df
    for func in func_queue:
        dataset = func(dataset)
    return dataset

def reorder_columns(df, new_order):
    return df.reindex(columns=new_order)

def aggregate_window_serieses(df, funcs, windows, func_names):
    _data_responce = None
    for window in windows:
        _subset = list(pd.DataFrame(df.iloc[:, -window:].apply(func, axis='columns')).rename({0:f'{func_names[idx]}_win_{window}'}, axis=1) for idx, func in enumerate(funcs))
        _subset = pd.concat(_subset, axis=1) 
        if _data_responce is None:
            _data_responce = _subset
        else:
            _data_responce = pd.concat([_data_responce, _subset], axis=1, join='inner')
    return _data_responce