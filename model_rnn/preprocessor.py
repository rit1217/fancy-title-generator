import unicodedata
import re
from .config import BOS, EOS, DATA_ALL_CHARS


def normalize_string(in_str:str) -> str:
    out = []
    for char in unicodedata.normalize('NFD', in_str.strip()):
        if unicodedata.category(char) != 'Mn' and char in DATA_ALL_CHARS:
            out.append(char)
    out = ''.join(out)
    out = re.sub(r' +', ' ', out)
    return BOS + out + EOS