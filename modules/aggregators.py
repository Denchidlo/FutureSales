from transformers import *

def take_subseries(df, columns, new_name):
    if isinstance(columns, list): 
        return df.loc[:, columns].rename(dict([zip(columns, new_name)]))
    else:
        return df.loc[:, df.columns[columns]].rename(dict(zip(df.columns[columns], new_name)), axis=1)

def create_aggregation_pipeline(df, func_queue):
    dataset = df
    for func in func_queue:
        dataset = func(dataset)
    return dataset

def reorder_columns(df, new_order):
    return df.reindex(columns=new_order)

def interact_df(set_1, set_2, func, new_names)