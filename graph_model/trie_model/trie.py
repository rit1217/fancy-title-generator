import json
from typing import TextIO
from .trie_node import TrieNode
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def add_data(self, new_suggestions):
        for suggestion in new_suggestions:
            self.root.insert(suggestion)

    
    def autocomplete(self, prefix, top_n):
        cur_node = self.root.find_node(prefix)
        
        if len(cur_node.children) < 1:
            return []

        result = []
        for i in cur_node.get_all_titles():
            result.append(i)

        # sort output titles by score
        result.sort(key=lambda item: item['score'], reverse=True)
        return result[:top_n]


    def save(self, fileobject: TextIO):
        self.root = self.root.to_dict()
        json.dump(self.__dict__, fileobject)


    def load(self, fileobject: TextIO):
        def init_trie_node(node_dict):
            node = TrieNode(node_dict['prefix'], node_dict['char'])
            node.score = node_dict['score']
            for c, d in node_dict['children'].items():
                node.children[c] = init_trie_node(d)
            return node
        
        self.root = init_trie_node(json.load(fileobject)['root'])
        return self