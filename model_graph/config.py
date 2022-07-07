import os


#File configs.
TEMP_DIR = 'temp/'
BUNDLE_LIST = []
FILENAMES = {
    'model': 'graph.model.json.gz',
}
FILEPATHS = {k: os.path.join(TEMP_DIR, v) for k, v in FILENAMES.items()}


#Data config.
DATA_SUBDIRS = ['item_master']
DATA_FILENAMES = {x: f'{x}.csv.gz' for x in DATA_SUBDIRS}
DATA_FILEPATHS = {k: os.path.join(TEMP_DIR, v) for k, v in DATA_FILENAMES.items()}