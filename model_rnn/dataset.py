import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as data
from .vectorize import make_input_vect
from .config import DATA_FILEPATHS
from .preprocessor import preprocess_text, CHAR_TO_IX


class Dataset(data.Dataset):
    def __init__(self):
        self.titles = pd.read_csv(DATA_FILEPATHS['item_master'], encoding='utf-8')['PRODUCT_NAME']\
            .dropna().apply(preprocess_text).astype(str).tolist()
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    def __len__(self):
        return len(self.titles)
    
    def __getitem__(self, index):
        return self.titles[index]

    def collate_fn(self, titles):
        X, y = [], []

        for name in titles:
            for c in range(1, len(name)):
                X.append(make_input_vect(name[:c]))
                y.append(CHAR_TO_IX[name[c]])
        X_lengths, X_indices = torch.tensor([len(x) for x in X],
            dtype=torch.int16, device=torch.device('cpu'), requires_grad=False)\
            .sort(descending=True)
        X = nn.utils.rnn.pad_sequence(X, batch_first=True)[X_indices]
        Z = nn.utils.rnn.pack_padded_sequence(X, X_lengths, batch_first=True)
        y = torch.tensor(y, dtype=torch.int64, device=self.device, requires_grad=False)[X_indices]

        return Z, y