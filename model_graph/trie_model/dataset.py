import pandas as pd
import re
from ..config import DATA_FILEPATH


class Dataset:
        
    def __init__(self):
        self.titles = [self.preprocess_title(x) for x in self.read_data()]


    def __iter__(self):
        return iter(self.titles)


    def read_data(self) -> list[str]:
        csv_file = pd.read_csv(DATA_FILEPATH)
        # drop NaN rows
        nan_value = float("NaN")
        csv_file.replace("", nan_value, inplace=True)
        csv_file.dropna(subset = ["PRODUCT_NAME"], inplace=True)
        return csv_file['PRODUCT_NAME'].values


    def preprocess_title(self, item_title:str) -> str:
        # remove unconsider characters from words in the sequence
        if type(item_title) == str:
            item_title = item_title.lower()
            item_title = re.sub(r'[^0-9a-z\-\s]', '', item_title)
            item_title = re.sub(r' +', ' ', item_title)
            item_title = item_title.strip()
            return item_title
    
