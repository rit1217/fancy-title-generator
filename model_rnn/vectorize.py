import torch
from .config import DATA_CHAR_TO_IX


def make_input_vect(title:str) -> torch.tensor:
    arr_name = torch.zeros(len(title), len(DATA_CHAR_TO_IX),
        dtype=torch.float32)
    for c, char in enumerate(title):
        arr_name[c][DATA_CHAR_TO_IX[char]] = 1
    return arr_name