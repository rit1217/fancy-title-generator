import pandas as pd
import re
from ..config import DATA_FILEPATHS


class Dataset:
    def __init__(self):
        self.titles = [self.preprocess_title(x) for x in self.read_data()]

    def __iter__(self):
        return iter(self.titles)

    def read_data(self) -> list[str]:
        return pd.read_csv(DATA_FILEPATHS['item_master'])['PRODUCT_NAME']\
            .dropna().astype(str).tolist()

    def preprocess_title(self, s:str) -> str:
        s = s.lower()
        s = re.sub(r'[^0-9a-z\- ]', '', s)
        s = re.sub(r' +', ' ', s)
        return s.strip()
