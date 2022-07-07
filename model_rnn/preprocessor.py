import unicodedata
import re
import string


BOS, EOS = '<', '>'
ALL_CHARS = BOS + string.ascii_letters + " .,;'-" + EOS
CHAR_TO_IX = {x: i for i, x in enumerate(ALL_CHARS)}
IX_TO_CHAR = {value: key for key, value in CHAR_TO_IX.items()}


def preprocess_text(in_str:str) -> str:
    out = []
    for char in unicodedata.normalize('NFD', in_str.strip()):
        if unicodedata.category(char) != 'Mn' and char in ALL_CHARS:
            out.append(char)
    out = ''.join(out)
    out = re.sub(r' +', ' ', out)
    return BOS + out + EOS