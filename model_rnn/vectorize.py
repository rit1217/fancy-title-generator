import torch
import torch.nn.functional as F
from .preprocessor import CHAR_TO_IX, IX_TO_CHAR, CATE_TO_IX


def make_input_vect(title:str, cate:str) -> torch.tensor:
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    arr_cate = torch.tensor([CATE_TO_IX[cate] for _ in title],
        dtype=torch.int64, device=device, requires_grad=False)
    oh_cate = F.one_hot(arr_cate, num_classes=len(CATE_TO_IX))
    arr = torch.tensor([CHAR_TO_IX[x] for x in title],
        dtype=torch.int64, device=device, requires_grad=False)
    
    oh_name = F.one_hot(arr, num_classes=len(CHAR_TO_IX))\
        .type(torch.float32)
    
    return torch.cat((oh_name, oh_cate), dim=1).type(torch.float32)

def concat_one_hot(prefix:torch.tensor, next_char_ix:int, cate:torch.tensor) -> torch.tensor:
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    arr_cate = torch.tensor([CATE_TO_IX[cate]],
        dtype=torch.int64, device=device, requires_grad=False)
    oh_cate = F.one_hot(arr_cate, num_classes=len(CATE_TO_IX))

    char_tensor = torch.tensor([next_char_ix], device=device)
    char_one_hot = F.one_hot(char_tensor, num_classes=len(IX_TO_CHAR)).type(torch.float32)
    temp = torch.cat((char_one_hot, oh_cate), dim=1).type(torch.float32)

    return torch.cat((prefix, temp), 0)

def devectorize(title_tensor:torch.tensor) -> str:
    labels = torch.argmax(title_tensor, dim = 1).tolist()
    title = ''
    for ix in labels:
        title += IX_TO_CHAR[ix]
    return title
