from sre_parse import CATEGORIES
import unicodedata
import re
import string


CATEGORIES = ['misc', 'bottoms', 'pants', 'none', 'stationary', 'jumpsuits & rompers', 'active jackets', 'dresses', 'skirts', 'workout shorts', 'jewelry', 'active tops', 'skirts and skorts', 'shorts', 'beauty', 'hats and hair', 'outerwear', 'swimwear', 'sports bras', 'activewear accessories', 'intimates', 'lifestyle', 'workout pants', 
'leggings', 'tops', 'scarves', 'bags & bag straps', 'sunglasses', 'belts', 'shoes']
BOS, EOS = '<', '>'
ALL_CHARS = BOS + string.ascii_letters + " .,;'-" + EOS
CHAR_TO_IX = {x: i for i, x in enumerate(ALL_CHARS)}
IX_TO_CHAR = {value: key for key, value in CHAR_TO_IX.items()}
CATE_TO_IX = {x: i for i, x in enumerate(CATEGORIES)}
IX_TO_CATE = {value: key for key, value in CATE_TO_IX.items()}

def preprocess_text(in_str:str) -> str:
    out = []
    for char in unicodedata.normalize('NFD', in_str.strip()):
        if unicodedata.category(char) != 'Mn' and char in ALL_CHARS:
            out.append(char)
    out = ''.join(out)
    out = re.sub(r' +', ' ', out)
    return BOS + out + EOS