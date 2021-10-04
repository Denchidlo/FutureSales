import numpy as np
import pandas as pd

def make_indexes(shops, categories):
    _preprocessing_pipeline = {
        'id_merging_stage': lambda dataset: dataset.merge(
                                    shops,
                                    how='cross'
                                ).merge(
                                    categories,
                                    on='item_category_id'
                                ).reset_index().rename({'index': 'id'}, axis=1),
    }
    return _preprocessing_pipeline


def make_task_df(items, shops, categories, index):
    _preprocessing_pipeline = {
        'id_merging_stage': lambda dataset: dataset.merge(
                                    items, 
                                    on='item_id'
                                ).merge(
                                    shops,
                                    on='shop_id'
                                ).merge(
                                    categories,
                                    on='item_category_id'
                                ),
        'summarizing_and_name_merging_stage': lambda dataset: dataset.groupby(
                                                    ['date', 'date_block_num', 'shop_id', 'item_category_id', 'item_id']
                                                ).agg({'item_cnt_day': np.sum, 'item_price': np.mean}).reset_index().sort_values('date'),
        'date_block_num_renaming': lambda dataset: dataset.rename(columns={'date_block_num': 'month_block'}, inplace=True),
        'object_id_encoding': lambda dataset: dataset.merge(
                                    index[['id', 'shop_id', 'item_id']], 
                                    on=['shop_id', 'item_id'])
    }
    return _preprocessing_pipeline