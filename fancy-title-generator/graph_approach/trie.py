class TrieNode:
    def __init__(self, parent = None):
        self.parent = parent
        self.children = {}
        self.is_leaf = True
    
    def insert(self, text):
        self.is_leaf = False
        if len(text) < 1:
            return
        
        word = text[0]
        if word not in self.children:
            self.children[word] = TrieNode(self)
        
        self.children[word].insert(text[1:])

    # return generator
    def leaves(self, prefix_path):
        if self.is_leaf:
            yield prefix_path
        else:
            for word, node in self.children.items():
                path = prefix_path + word
                for leaf in node.leaves(path):
                    yield leaf


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def index(self, new_suggestions):
        for suggestion in new_suggestions:
            self.root.insert(suggestion)

    def search(self, prefix):
        result = self.root.find(prefix)

        if result == None:
            return None
        
        return result.leaves(prefix)