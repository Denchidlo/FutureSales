import pandas as pd
import numpy as np

from collections import namedtuple
from enum import Enum


class ExpandedWindowIterator:
    """
    ExpandedWindowIterator - generator used for expanding window dataset spliting

    Args:
        - target_column -> Column used for slice creation
        - min_idx -> Entry point for target_column
        - final_idx -> End point for target_column
        - step -> step_size for target value

    Example:

    >>> iteration_rule = ExpandedWindowIterator(target_column='date_block_num', min_idx=1, step=2, max_idx=4)

    >>> for idx, split in iteration_rule(df):
    >>>    validation_pipeline(split)
    """

    def __init__(
        self,
        target_column,
        target_vector_extractor,
        min_idx=None,
        step=None,
        max_idx=None,
    ):
        self._cfg = {
            "extractor": target_vector_extractor,
            "target_column": target_column,
            "min": min_idx,
            "max": max_idx,
            "step_size": step,
        }

    def __call__(self, dataset, min_idx=None, step=None, max_idx=None):
        if not (min_idx == step == max_idx == None):
            self._cfg["min"] = min_idx
            self._cfg["max"] = max_idx
            self._cfg["step_size"] = step

        target_key = self._cfg["target_column"]

        if not target_key in dataset.columns:
            raise IndexError(f"{target_key} is not in columns")

        _min = self._cfg["min"]
        _max = self._cfg["max"]
        _step = self._cfg["step_size"]

        if _min == _step == _max == None:
            raise ValueError(f"'None' was found in (min_idx, step, max_idx)")
        if dataset[target_key].min() >= _min or dataset[target_key].max() < _max:
            raise ValueError(f"Target value is out of bounds")

        target_extractor = self._cfg["extractor"]

        idx = _min
        while idx < _max - _step:
            y_val = target_extractor(idx)
            features = dataset[dataset[target_key] <= idx]

            yield idx, features, y_val

            idx += _step

        y_val = target_extractor(idx + 1)
        features = dataset[dataset[target_key] <= idx]

        yield idx, features, y_val

        if idx < _max:
            y_val = target_extractor(_max)
            features = dataset[dataset[target_key] <= _max]

            yield _max, features, y_val

class EntityIterator:
    """
    EntityIterator - generator used for observing separate id's

    Example:

    >>> iteration_rule = ExpandedWindowIterator(target_column='date_block_num', min_idx=1, step=2, max_idx=4)
    >>> subset_extractor = EntityIteratot('id')

    >>> for window, split in iteration_rule(df):
    >>>    for _id, subset in subset_extractor(split):
    >>>        feature_df[encode_pair(window, _id)] = create_feature_vector(subset, recipe)
    """

    def __init__(self, idx):
        self._idx = idx

    def __call__(self, df):
        idxs = df.loc[:, self._idx]
        for unique in idxs.unique():
            yield unique, df[idxs == unique]


class SampleIterator:
    def __init__(self, idx, **pd_sample_options):
        self._idx = idx
        self._sample_options = pd_sample_options

    def __call__(self, df):
        idxs = df.loc[:, self._idx]
        for unique in pd.Series(idxs.unique()).sample(**self._sample_options):
            yield unique, df[idxs == unique]