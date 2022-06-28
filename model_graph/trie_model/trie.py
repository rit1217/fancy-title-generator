import json
from typing import TextIO
from .trie_node import TrieNode


class Trie:
    def __init__(self):
        self.root = TrieNode('')

    def add_data(self, new_titles:list[str]):
        for title in new_titles:
            self.root.insert(title)

    def autocomplete(self, prefix:str, top_n:int=5) -> list[dict]:
        result = []
        cur_node = self.root.find_node(prefix)

        if cur_node is not None:
            for i in cur_node.get_all_titles(prefix):
                result.append(i)
            # sort output titles by score
            result.sort(key=lambda item: item.score, reverse=True)
            result = [title_obj._asdict() for title_obj in result[:top_n] ]

        return result

    def save(self, fileobj: TextIO):
        self.root = self.root.to_dict()
        json.dump({
            'char' : self.root['char'],
            'score': self.root['score'],
            'children': self.root['children']
        }, fileobj)

    def _init_trie_node(self, node_dict:dict):
        node = TrieNode( node_dict['char'], node_dict['score'], {})
        for char, child_dict in node_dict['children'].items():
            node.children[char] = self._init_trie_node(child_dict)
        return node

    def load(self, fileobject: TextIO):     
        self.root = self._init_trie_node(json.load(fileobject))
        return self