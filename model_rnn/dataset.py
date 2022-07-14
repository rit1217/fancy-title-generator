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
        self.X, self.y = [], []
        self.pad_input_size = (0, len(CHAR_TO_IX))

        for name in self.titles:
            for c in range(1, len(name)):
                name_vec = make_input_vect(name[0:c])
                if name_vec.size()[0] > self.pad_input_size[0]:
                    self.pad_input_size = (name_vec.size()[0], len(CHAR_TO_IX))
                self.X.append(make_input_vect(name[0:c]))
                self.y.append(name[c])
        self.y = torch.tensor([CHAR_TO_IX[char] for char in self.y],
            dtype=torch.int64, requires_grad=False)
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, index):
        return F.pad(self.X[index], (0, self.pad_input_size[1] - self.X[index].size()[1],
                                      0, self.pad_input_size[0] - self.X[index].size()[0] )),self.y[index]