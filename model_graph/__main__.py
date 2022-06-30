from .model import GraphModel as Model
from .trie_model import Dataset

data = Dataset()
Model().train(data).save()