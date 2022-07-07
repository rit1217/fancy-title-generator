import torch
import torch.nn.functional as F
from .preprocessor import CHAR_TO_IX


def make_input_vect(title:str) -> torch.tensor:
    char_ix_arr = []
    for char in title:
        char_ix_arr.append(CHAR_TO_IX[char])
    return F.one_hot(torch.tensor(char_ix_arr),num_classes=len(CHAR_TO_IX)).type(torch.float32)