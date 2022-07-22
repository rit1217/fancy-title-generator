import torch
import torch.nn.functional as F
from .preprocessor import CHAR_TO_IX, IX_TO_CHAR


def make_input_vect(title:str) -> torch.tensor:
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    arr = torch.tensor([CHAR_TO_IX[x] for x in title],
        dtype=torch.int64, device=device, requires_grad=False)
    return F.one_hot(arr, num_classes=len(CHAR_TO_IX))\
        .type(torch.float32)

def concat_one_hot(prefix:torch.tensor, next_char_ix:int) -> torch.tensor:
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    char_tensor = torch.tensor([next_char_ix], device=device)
    char_one_hot = F.one_hot(char_tensor, num_classes=len(IX_TO_CHAR)).type(torch.float32)
    return torch.cat((prefix, char_one_hot), 0)

def devectorize(title_tensor:torch.tensor) -> str:
    labels = torch.argmax(title_tensor, dim = 1).tolist()
    title = ''
    for ix in labels:
        title += IX_TO_CHAR[ix]
    return title
