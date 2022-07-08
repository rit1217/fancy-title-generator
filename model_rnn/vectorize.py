import torch
import torch.nn.functional as F
from .preprocessor import CHAR_TO_IX


def make_input_vect(title:str) -> torch.tensor:
    arr = torch.tensor([CHAR_TO_IX[c] for x in title],
        dtype=torch.int64, device=torch.device('cpu'), requires_grad=False)
    return F.one_hot(arr, num_classes=len(CHAR_TO_IX))\
        .type(torch.float32)