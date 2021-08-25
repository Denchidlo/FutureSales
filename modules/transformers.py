import numpy as np
import pandas as pd


def make_transformer(func, **kwargs):
    def wrapped(serieses):
        return func(serieses, **kwargs)
    return wrapped


class FeatureExtractor:

    class _Extractor:
        def __init__(self, tasks) -> None:
            self._context = {
                'tasks': tasks,
            }
            self._results = {}

        def fit(self, df):
            self._context['df'] = df
            self._results = {}

            for subset in self._context['tasks']['iterator'](df):
                self._create_serieses()
                self._extract_features()
                self._append_to_result()

        def _get_serieses(self, names):
            for name in names:
                if name in self._results['serieses']:
                    return self._results['serieses'][name]
                else:
                    return self._context['df'][name]

        def _create_serieses(self):
            self._results['serieses'] = {}
            for task_name, handler in self._context['tasks']['serieses'].items():
                affected_serieses = self._get_serieses(handler['serieses'])
                self._results['serieses'][task_name] = handler['executor'](*affected_serieses)


        def _extract_features(self):
            pass


    def __init__(self, subseries_cfg, feature_cfg, entity_iterator) -> None:
        self._tasks = {
            'subserieses': self._process_subseries_cfg(subseries_cfg),
            'features': self._process_feature_cfg(feature_cfg),
            'iterator': entity_iterator
        }

    @staticmethod
    def _process_subseries_cfg(self, cfg):
        translated = {}
        for task_name, encoded_task in cfg:
            translated[task_name] = {
                'executor': make_transformer(FUNC_MAP[encoded_task['func_name']], **encoded_task['params']),
                'serieses': encoded_task['series_order'],
            }
        return translated

    @staticmethod
    def _process_feature_cfg(self, cfg):
        translated = {}
        for task in cfg:
            translated[task] = {
                'executor': make_transformer(FUNC_MAP[task['func_name']], **task['params']),
                'from': task['from'],
            }
        return translated

    def __call__(self, df):
        return self._Extractor(df, self._tasks)




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