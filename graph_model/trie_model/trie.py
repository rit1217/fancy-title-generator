import json
from graph_model.trie_model.trie_node import TrieNode
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def add_data(self, new_suggestions):
        for suggestion in new_suggestions:
            self.root.insert(suggestion)

    def get_next_char(self, prefix):
        result = self.root.find_node(prefix)

        if result == None:
            return []
        
        return result.get_sorted_children(prefix)

    
    def autocomplete(self, prefix, top_n):
        cur_node = self.root.find_node(prefix)
        
        if len(cur_node.children) < 1:
            return []

        result = []
        for i in cur_node.get_all_titles():
            result.append(i)

        # sort output titles by score
        result.sort(key=lambda item: item['score'], reverse=True)
        print('Normalx search ->\nConsidered: ', len(result), result[:3], '\nPrefix: ',prefix)
        return result[:top_n]

    def to_dict(self):
        self.root = self.root.to_dict()
        print(type(self.root))
        return self.__dict__

    def load(self, json_dict):
        def init_trie_node(node_dict):
            node = TrieNode(node_dict['prefix'], node_dict['char'])
            node.score = node_dict['score']
            for c, d in node_dict['children'].items():
                node.children[c] = init_trie_node(d)
            return node
        
        self.root = init_trie_node(json_dict['root'])
        return self