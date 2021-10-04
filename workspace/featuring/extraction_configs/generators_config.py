from futuresales.features import *
from futuresales.distribution import from_pickle

def make_baseline_train_generator(train_max):
    _gen_cfg = {
        'id_sales': {
            'series_order': [],
            'func_name': from_pickle,
            'params': {
                'path': '../tmp/id_sales.pkl'
            }
        },
        # 'id_sales': {
        #     'series_order': ['original'],
        #     'func_name': extract_id_sequences,
        #     'params': {
        #         'index': ['id'],
        #         'seq_index': ['month_block'],
        #         'target': 'item_cnt_day',
        #         'aggregator': np.sum,
        #         'fill_na': 0,
        #     }
        # },
        # 'id_sales_test': {
        #     'series_order': ['test'],
        #     'func_name': extract_id_sequences,
        #     'params': {
        #         'index': ['id'],
        #         'seq_index': ['month_block'],
        #         'target': 'item_cnt_day',
        #         'aggregator': np.sum,
        #         'fill_na': 0,
        #     }
        # },
        'id_sales_test': {
            'series_order': [],
            'func_name': from_pickle,
            'params': {
                'path': '../tmp/id_sales_test.pkl'
            }
        },
        'train_series': {
            'series_order': ['id_sales'],
            'func_name': take_subseries,
            'params': { 
                'columns': slice(None, train_max - 33) if train_max != 33 else slice(None, None), 
                'new_name': [i for i in range(train_max + 1)]
            }
        },
        'diff_1': {
            'series_order': ['train_series'], 
            'func_name': diff,
            'params': {
                'order': 1
            }
        },
        'diff_2': {
            'series_order': ['train_series'], 
            'func_name': diff,
            'params': {
                'order': 2
            }
        },
        'lags': {
            'series_order': ['train_series'],
            'func_name': create_aggregation_pipeline,
            'params': {
                'func_queue': [
                    make_transformer(
                        take_subseries, 
                        columns=slice(-12, None), 
                        new_name=[f'lag_{12 - i}' for i in range(0, 12)]),
                    make_transformer(
                        reorder_columns,
                        new_order=[f'lag_{i}' for i in range(1, 13)])
                ]
            }
        },
        'lags_12': {
            'series_order': ['train_series'],
            'func_name': create_aggregation_pipeline,
            'params': {
                'func_queue': [
                    make_transformer(
                        take_subseries, 
                        columns=slice(-24, -12), 
                        new_name=[f'lag_12_{12 - i}' for i in range(0, 12)]),
                    make_transformer(
                        reorder_columns,
                        new_order=[f'lag_12_{i}' for i in range(1, 13)])
                ]
            }
        },
    }
    return _gen_cfg