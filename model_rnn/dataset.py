import pandas as pd
import torch
import torch.nn as nn
import torch.utils.data as data
from .vectorize import make_input_vect
from .config import DATA_FILEPATHS
from .preprocessor import preprocess_text, CHAR_TO_IX


class Dataset(data.Dataset):
    def __init__(self):
        self.titles = pd.read_csv(DATA_FILEPATHS['item_master'])['PRODUCT_NAME']\
            .dropna().apply(preprocess_text).astype(str).tolist()
        self.X, self.y = [], []
        for name in self.titles:
            for c in range(1, len(name)):
                self.X.append(make_input_vect(name[0:c]))
                self.y.append(name[c])
        X_lengths, X_indexes = torch.tensor([len(x) for x in self.X],
            dtype=torch.int16, requires_grad=False).sort(descending=True)
        self.X = nn.utils.rnn.pad_sequence(self.X, batch_first=True)[X_indexes]
        self.y = torch.tensor([CHAR_TO_IX[char] for char in self.y],
            dtype=torch.int64, requires_grad=False)[X_indexes]
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, index):
        return self.X[index], self.y[index]