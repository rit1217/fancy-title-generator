import gzip
from .trie_model import Trie, Dataset
from .config import MODEL_FILEPATH


class GraphModel:
    def __init__(self):
        self.trie = Trie()

    def train(self, data:Dataset):
        self.trie.add_data(data)
        return self

    def load(self):
        with gzip.open(MODEL_FILEPATH, 'rt') as f:
            self.trie.load(f)
        return self

    def save(self):
        with gzip.open(MODEL_FILEPATH, 'wt') as f:
            self.trie.save(f)

    def predict(self, prefix:str='', top_n:int=5) -> list:
        return self.trie.autocomplete( prefix, top_n)