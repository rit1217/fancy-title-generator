import pandas as pd
import re
import string
import unicodedata
import torch
import numpy as np
import torch.nn as nn
from .scripts import make_input_vect
from .config import DATA_FILEPATH, DEVICE
from .config import DATA_ALL_CHARS, DATA_CHAR_START, DATA_CHAR_END, DATA_CHAR_TO_IX


class Dataset:
    def __init__(self):
        self.titles = [self.normalize_title(x) for x in self.read_data()]
        self.preprocess()

    def __iter__(self):
        return iter(self.titles)

    def read_data(self) -> list[str]:
        return pd.read_csv(DATA_FILEPATH)['PRODUCT_NAME']\
            .dropna().astype(str).tolist()

    def normalize_title(self, s:str) -> str:
        s = []
        for char in unicodedata.normalize('NFD', string.strip()):
            if unicodedata.category(char) != 'Mn' and char in DATA_ALL_CHARS:
                s.append(char)
        s = ''.join(s)
        s = re.sub(r' +', ' ', s)
        return DATA_CHAR_START + s + DATA_CHAR_END

    def preprocess(self):
        rand_idx = np.random.RandomState(seed=0).permutation(len(self.titles))
        self.titles = np.array(self.titles)[rand_idx.tolist()]

        n_test = len(names) // 10
        names, names_t = names[0:-n_test], names[-n_test:]

        self.X, self.y = [], []
        for name in self.titles:
            for c in range(1, len(name)):
                self.X.append(make_input_vect(name[0:c]))
                self.y.append(name[c])
        # torch.tensor return as values and indices
        X_lengths, X_indexes = torch.tensor([len(x) for x in self.X],
            dtype=torch.int16, device=DEVICE, requires_grad=False).sort(descending=True)
        self.X = nn.utils.rnn.pad_sequence(self.X, batch_first=True)[X_indexes]
        self.Z = nn.utils.rnn.pack_padded_sequence(self.X, X_lengths.to('cpu'), batch_first=True)
        self.y = torch.tensor([DATA_CHAR_TO_IX[char] for char in self.y],
            dtype=torch.int64, device=DEVICE, requires_grad=False)[X_indexes]


        self.Xt, self.yt = [], []
        for name in names_t:
            for c in range(1, len(name)):
                self.Xt.append(make_input_vect(name[0:c]))
                self.yt.append(name[c])
        Xt_lengths, Xt_indexes = torch.tensor([len(x) for x in self.Xt],
            dtype=torch.int16, device=DEVICE, requires_grad=False).sort(descending=True)
        self.Xt = nn.utils.rnn.pad_sequence(self.Xt, batch_first=True)[Xt_indexes]
        self.Zt = nn.utils.rnn.pack_padded_sequence(self.Xt, Xt_lengths.to('cpu'), batch_first=True)
        self.yt = torch.tensor([DATA_CHAR_TO_IX[char] for char in self.yt],
            dtype=torch.int64, device=DEVICE, requires_grad=False)[Xt_indexes]
