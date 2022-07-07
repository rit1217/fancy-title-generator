import os
import string
import logging
from pathlib import Path


# Configure logging.
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO,
    force=True,
)


# File configs.
TEMP_DIR = 'temp/'
DATA_DIR = os.path.join(TEMP_DIR, 'data')
MODEL_DIR = os.path.join(TEMP_DIR, 'model')
for dir in [DATA_DIR, MODEL_DIR]:
    Path(dir).mkdir(parents=True, exist_ok=True)

BUNDLE_LIST = []
FILENAMES = {
    'model': 'rnn.model',
}
FILEPATHS = {k: os.path.join(MODEL_DIR, v) for k, v in FILENAMES.items()}


# Data config.
DATA_SUBDIRS = ['item_master']
DATA_FILENAMES = {x: f'{x}.csv.gz' for x in DATA_SUBDIRS}
DATA_FILEPATHS = {k: os.path.join(DATA_DIR, v) for k, v in DATA_FILENAMES.items()}

BOS, EOS = '<', '>'
DATA_ALL_CHARS = BOS + string.ascii_letters + " .,;'-" + EOS
DATA_N_CHARS = len(DATA_ALL_CHARS)
DATA_CHAR_TO_IX = {x: i for i, x in enumerate(DATA_ALL_CHARS)}
DATA_IX_TO_CHAR = {value: key for key, value in DATA_CHAR_TO_IX.items()}
