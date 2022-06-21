from api.trie_model.trie_node import TrieNode
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def add_data(self, new_suggestions):
        for suggestion in new_suggestions:
            self.root.insert(suggestion)

    def get_next_char(self, prefix):
        result = self.root.find_leaf(prefix)

        if result == None:
            return []
        
        return result.get_sorted_children(prefix)

    def autocomplete(self, prefix):
        cur_node = self.root
        for word in prefix:
            if word not in cur_node.children.keys():
                return []
            cur_node = cur_node.children[word]
 
        
        if len(cur_node.children) < 1:
            return []

        result = []
        for i in cur_node.suggest_whole_title(prefix):
            result.append(i)
        result.sort(key=lambda item: item['score'], reverse=True)
        print('Normalx search ->\nConsidered: ', len(result), result[:3], '\nPrefix: ',prefix)
        return result