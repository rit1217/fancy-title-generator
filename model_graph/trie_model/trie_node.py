class TrieNode:

    def __init__(self, char:str, score:int=1, children:dict=None):
        if children:
            self.children = children
        else:
            self.children = {}
        self.char = char
        self.score = score


    def insert(self, text):
        if len(text) < 1:
            return
        
        character = text[0]
        if character not in self.children:
            self.children[character] = TrieNode(character, 1, {})
        else:
            self.children[character].score += 1
        
        self.children[character].insert(text[1:])

    
    def find_node(self, path:str):
        if len(path) < 1:
            return self

        character = path[0]

        if character in self.children:
            return self.children[character].find_node(path[1:])
        else:
            return None
 

    def get_all_titles(self, prefix:str):
        if len(self.children) < 1:
            yield {"title": prefix, "score":self.score}
        else:
            for char, node in self.children.items():
                for title in node.get_all_titles(prefix + char):
                    yield title


    def to_dict(self):
        if len(self.children) < 1:
            return {
            'char' : self.char,
            'score': self.score,
            'children': self.children
        }
        children_dict = {}
        for char, node in self.children.items():
            children_dict[char] = node.to_dict()
        self.children = children_dict
        return {
            'char' : self.char,
            'score': self.score,
            'children': self.children
        }