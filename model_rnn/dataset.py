import pandas as pd
import re
import string
import unicodedata
import torch
import torch.nn as nn
import torch.utils.data as data
from .vectorize import make_input_vect
from .config import DATA_FILEPATH
from .config import DATA_ALL_CHARS, BOS, EOS, DATA_CHAR_TO_IX


class Dataset(data.Dataset):
    def __init__(self):
        self.titles = [self._normalize_title(x) for x in self.read_data()]
        self.preprocess()

    def __iter__(self):
        return iter(self.titles)
    
    def __len__(self):
        return len(self.titles)
    
    def __getitem__(self, index):
        return make_input_vect(self.titles[index])

    def read_data(self) -> list[str]:
        return pd.read_csv(DATA_FILEPATH)['PRODUCT_NAME']\
            .dropna().astype(str).tolist()

    def _normalize_title(self, s:str) -> str:
        s = []
        for char in unicodedata.normalize('NFD', string.strip()):
            if unicodedata.category(char) != 'Mn' and char in DATA_ALL_CHARS:
                s.append(char)
        s = ''.join(s)
        s = re.sub(r' +', ' ', s)
        return BOS + s + EOS

    def preprocess(self):
        self.X, self.y = [], []
        for name in self.titles:
            for c in range(1, len(name)):
                self.X.append(make_input_vect(name[0:c]))
                self.y.append(name[c])
        X_lengths, X_indexes = torch.tensor([len(x) for x in self.X],
            dtype=torch.int16, requires_grad=False).sort(descending=True)
        self.X = nn.utils.rnn.pad_sequence(self.X, batch_first=True)[X_indexes]
        self.X = nn.utils.rnn.pack_padded_sequence(self.X, X_lengths.to('cpu'), batch_first=True)
        self.y = torch.tensor([DATA_CHAR_TO_IX[char] for char in self.y],
            dtype=torch.int64, requires_grad=False)[X_indexes]
        return self.X, self.y