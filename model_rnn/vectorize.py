import torch
import torch.nn.functional as F
from .preprocessor import CHAR_TO_IX


def make_input_vect(title:str) -> torch.tensor:
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    arr = torch.tensor([CHAR_TO_IX[x] for x in title],
        dtype=torch.int64, device=device, requires_grad=False)
    return F.one_hot(arr, num_classes=len(CHAR_TO_IX))\
        .type(torch.float32)