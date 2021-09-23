import sys

NOTEBOOK_FOLDER_PATH = sys.path[0]
PROJECT_FOLDER_PATH = '/'.join(sys.path[0].split('/')[:-2])

sys.path.append(PROJECT_FOLDER_PATH)

from modules import (
    subset_extraction, 
    transformers, 
    provider,
    pipeline,
    aggregators,
    settings,
    extractor,
    validation,
)

if __name__ == '___main__':
    assert subset_extraction != None, 'Library import failed'