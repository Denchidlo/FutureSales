import os
from typing import Iterable
import pandas as pd

class DatasetProvider:
    def __init__(self, file_formats: Iterable[str]=['csv']):
        self.cwd = os.getcwd()
        self.file_list = []
        for dirname, _, filenames in os.walk(self.cwd):
            for filename in filenames:
                if filename.split('.')[-1] in file_formats:
                    self.file_list.append(os.path.join(dirname, filename))
        return None

    def get_dataset(self, path: str=None):
        if path == None:
            self._frames = {}
            for file in self.file_list:
                _ds_name = file.split('/')[-1]
                self._frames[_ds_name] = pd.read_csv(file)
        else:
            self._frames = pd.read_csv(path)
        return self._frames


class DatasetUploader:
    def __init__(self, path) -> None:
        self._path = path

    def save(self, dataset: pd.DataFrame, filename: str) -> None:
        try:
            with open(os.path.join(self._path, filename), 'w+') as writer:
                dataset.to_csv(writer)
        except:
            raise