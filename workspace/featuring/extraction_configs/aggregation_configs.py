from futuresales.features import *

def make_baseline_train_aggregation(train_max):
    _agg_cfg = {
        'valid_target': {
            'from': ['id_sales_test'],
            'func_name': take_subseries,
            'params': {
                'columns': slice(train_max-33, train_max-32) if train_max - 32 != 0 else slice(train_max-33, None),
                'new_name': ['valid_target'],
            },
        },
        'target': {
            'from': ['id_sales'],
            'func_name': take_subseries,
            'params': {
                'columns': slice(train_max-33, train_max-32) if train_max - 32 != 0 else slice(train_max-33, None),
                'new_name': ['target'],
            },
        },
        'lags': {
            'from': ['lags'],
            'func_name': take_subseries,
            'params': {
                'columns': [f'lag_{i}' for i in [1, 2, 3, 4, 6, 12]],
                'new_name': [f'lag_{i}' for i in [1, 2, 3, 4, 6, 12]],
            },
        },
        'dynamic_aggregation': {
            'from': ['train_series'],
            'func_name': aggregate_window_serieses,
            'params': {
                'funcs': [
                    'mean', 
                    'std',
                    'min',
                    'max',
                    ],
                'windows': [2, 4, 6, 12, train_max + 1],
                'func_names': [
                    'mean',
                    'std',
                    'min',
                    'max',
                    ]
            },
        },
        'diff_1_aggregation': {
            'from': ['diff_1'],
            'func_name': aggregate_window_serieses,
            'params': {
                'funcs': [
                    'mean', 
                    'std',
                    'min',
                    'max',
                    ],
                'windows': [2, 4, 6, 12],
                'func_names': [
                    'mean',
                    'std',
                    'min',
                    'max',
                    ]
            },
        },
        'diff_2_aggregation': {
            'from': ['diff_2'],
            'func_name': aggregate_window_serieses,
            'params': {
                'funcs': [
                    'mean', 
                    'std',
                    'min',
                    'max',
                    ],
                'windows': [2, 4, 6, 12],
                'func_names': [
                    'mean',
                    'std',
                    'min',
                    'max',
                    ]
            },
        },
        'lags_12_aggregation': {
            'from': ['lags_12'],
            'func_name': aggregate_window_serieses,
            'params': {
                'funcs': [
                    'mean', 
                    'std',
                    'min',
                    'max',
                    ],
                'windows': [2, 4, 6, 12],
                'func_names': [
                    'mean',
                    'std',
                    'min',
                    'max',
                    ]
            },
        },
    }
    return _agg_cfg

def make_baseline_submission_aggregation():
    _agg_cfg = {
        'lags': {
            'from': ['lags'],
            'func_name': take_subseries,
            'params': {
                'columns': [f'lag_{i}' for i in [1, 2, 3, 4, 6, 12]],
                'new_name': [f'lag_{i}' for i in [1, 2, 3, 4, 6, 12]],
            },
        },
        'dynamic_aggregation': {
            'from': ['train_series'],
            'func_name': aggregate_window_serieses,
            'params': {
                'funcs': [
                    'mean', 
                    'std',
                    'min',
                    'max',
                    ],
                'windows': [2, 4, 6, 12, 33],
                'func_names': [
                    'mean',
                    'std',
                    'min',
                    'max',
                    ]
            },
        },
        'diff_1_aggregation': {
            'from': ['diff_1'],
            'func_name': aggregate_window_serieses,
            'params': {
                'funcs': [
                    'mean', 
                    'std',
                    'min',
                    'max',
                    ],
                'windows': [2, 4, 6, 12],
                'func_names': [
                    'mean',
                    'std',
                    'min',
                    'max',
                    ]
            },
        },
        'diff_2_aggregation': {
            'from': ['diff_2'],
            'func_name': aggregate_window_serieses,
            'params': {
                'funcs': [
                    'mean', 
                    'std',
                    'min',
                    'max',
                    ],
                'windows': [2, 4, 6, 12],
                'func_names': [
                    'mean',
                    'std',
                    'min',
                    'max',
                    ]
            },
        },
        'lags_12_aggregation': {
            'from': ['lags_12'],
            'func_name': aggregate_window_serieses,
            'params': {
                'funcs': [
                    'mean', 
                    'std',
                    'min',
                    'max',
                    ],
                'windows': [2, 4, 6, 12],
                'func_names': [
                    'mean',
                    'std',
                    'min',
                    'max',
                    ]
            },
        },
    }
    return _agg_cfg