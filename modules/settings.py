from .extractor import *


AGGREGATION_CFG = {
    'lags': {
        'from': ['lags'],
        'func_name': take_subseries,
        'params': {
            'columns': [f'lag_{i}' for i in [1, 2, 3, 4, 6, 12]],
            'new_name': [f'lag_{i}' for i in [1, 2, 3, 4, 6, 12]],
        },
        'final_columns': [f'lag_{i}' for i in [1, 2, 3, 4, 6, 12]]
    },
    # 'percentiles': {
        
    # },
    # 'lag_aggregation': {
        
    # },
    # 'dynamic_aggregation': {

    # },
    # 'diff_1_aggregation': {

    # },
    # 'diff_2_aggregation': {

    # },
    # 'common_information': {

    # }
}


GENERATOIN_CFG = {
    'id_sales': {
        'series_order': ['original'],
        'func_name': extract_id_sequences,
        'params': {
            'index': ['id'],
            'seq_index': ['month_block'],
            'target': 'item_cnt_day',
            'aggregator': np.sum,
            'fill_na': 0,
        }
    },
    'diff_1': {
        'series_order': ['id_sales'], 
        'func_name': diff,
        'params': {
            'order': 1
        }
    },
    'diff_2': {
        'series_order': ['id_sales'], 
        'func_name': diff,
        'params': {
            'order': 2
        }
    },
    'acf': {
        'series_order': ['id_sales'], 
        'func_name': subset2subset,
        'params': {
            'series_transformer': make_transformer(take_acf, nlags=12),
            'column_names': [f'series_acf_{i}' for i in range(1, 13)]
        }
    },
    'lags': {
        'series_order': ['id_sales'],
        'func_name': create_aggregation_pipeline,
        'params': {
            'func_queue': [
                make_transformer(
                    take_subseries, 
                    columns=slice(-13, -1), 
                    new_name=[f'lag_{13 - i}' for i in range(1, 13)]),
                make_transformer(
                    reorder_columns,
                    new_order=[f'lag_{i}' for i in range(1, 13)])
            ]
        }
    },
    'lags_acf_raw': {
        'series_order': ['lags', 'acf'],
        'func_name': np.multiply,
        'params': {}
    },
    'lags_acf': {
        'series_order': ['lags_acf_raw'],
        'func_name': take_subseries,
        'params': {
            'columns':slice(None, None, None), 
            'new_name':[f'acf_lag_{i}' for i in range(1, 13)],
        }
    },
    'percentiles': {
        'series_order': ['id_sales'],
        'func_name': take_percentiles,
        'params': {
            'percentiles': [75, 90, 20, 40],
            'idx': 'month_block',
            'month': 32
        }
    }
}