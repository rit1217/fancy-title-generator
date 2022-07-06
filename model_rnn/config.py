import os
import torch
import string


#File configs.
TEMP_DIR = '../temp/'
DATA_FILENAME = 'item_master.csv.gz'
DATA_FILEPATH = os.path.join(TEMP_DIR, DATA_FILENAME)
MODEL_FILENAME = 'rnn.model'
MODEL_FILEPATH = os.path.join(TEMP_DIR, MODEL_FILENAME)


#Training configs.
DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


#Model configs.
MODEL_STOP_EPOCH = 15
MODEL_MAX_TRAIN_EPOCH = 999


#Data config.
DATA_CHAR_START, DATA_CHAR_END = '<', '>'
DATA_ALL_CHARS = DATA_CHAR_START + string.ascii_letters + " .,;'-" + DATA_CHAR_END
DATA_N_CHARS = len(DATA_ALL_CHARS)
DATA_CHAR_TO_IX = {x: i for i, x in enumerate(DATA_ALL_CHARS)}
DATA_IX_TO_CHAR = {value: key for key, value in DATA_CHAR_TO_IX.items()}
