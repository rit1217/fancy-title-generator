import os
import string


#File configs.
TEMP_DIR = 'temp/'
DATA_FILENAME = 'item_master.csv.gz'
DATA_FILEPATH = os.path.join(TEMP_DIR, DATA_FILENAME)
MODEL_FILENAME = 'rnn.model'
MODEL_FILEPATH = os.path.join(TEMP_DIR, MODEL_FILENAME)


#Data config.
BOS, EOS = '<', '>'
DATA_ALL_CHARS = BOS + string.ascii_letters + " .,;'-" + EOS
DATA_N_CHARS = len(DATA_ALL_CHARS)
DATA_CHAR_TO_IX = {x: i for i, x in enumerate(DATA_ALL_CHARS)}
DATA_IX_TO_CHAR = {value: key for key, value in DATA_CHAR_TO_IX.items()}
