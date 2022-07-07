import os
import logging


# Configure logging.
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO,
    force=True,
)


# File configs.
TEMP_DIR = 'temp/'
BUNDLE_LIST = []
FILENAMES = {
    'model': 'rnn.model',
}
FILEPATHS = {k: os.path.join(TEMP_DIR, v) for k, v in FILENAMES.items()}


# Data config.
DATA_SUBDIRS = ['item_master']
DATA_FILENAMES = {x: f'{x}.csv.gz' for x in DATA_SUBDIRS}
DATA_FILEPATHS = {k: os.path.join(TEMP_DIR, v) for k, v in DATA_FILENAMES.items()}