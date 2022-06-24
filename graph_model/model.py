import graph_model.trie_model as trie_model
from .config import MODEL_FILEPATH
class GraphModel:
    def __init__(self):
        self.trie = trie_model.Trie()

    def train(self, data):
        self.trie.add_data(data)
        return self

    def load(self):
        with open(MODEL_FILEPATH, 'rt') as f:
            self.trie.load(f)
        return self

    def save(self):
        with open(MODEL_FILEPATH, 'wt') as f:
            self.trie.save(f)

    def predict(self, prefix:str='', top_n:int=5) -> list:
        return self.trie.autocomplete( prefix, top_n)
        