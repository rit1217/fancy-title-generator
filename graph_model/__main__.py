from .model import GraphModel
import graph_model.trie_model as trie_model

trie_model.Dataset().save()
GraphModel().train().save()