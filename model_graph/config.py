import os
from pathlib import Path


#File configs.
TEMP_DIR = 'temp/'
DATA_DIR = os.path.join(TEMP_DIR, 'data')
MODEL_DIR = os.path.join(TEMP_DIR, 'model')
for dir in [DATA_DIR, MODEL_DIR]:
    Path(dir).mkdir(parents=True, exist_ok=True)

BUNDLE_LIST = []
FILENAMES = {
    'model': 'graph.model.json.gz',
}
FILEPATHS = {k: os.path.join(MODEL_DIR, v) for k, v in FILENAMES.items()}


#Data config.
DATA_SUBDIRS = ['item_master']
DATA_FILENAMES = {x: f'{x}.csv.gz' for x in DATA_SUBDIRS}
DATA_FILEPATHS = {k: os.path.join(DATA_DIR, v) for k, v in DATA_FILENAMES.items()}