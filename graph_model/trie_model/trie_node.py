from numpy import char

class TrieNode:
    def __init__(self, prefix = '', char = ''):
        self.children = {}
        self.char = char
        self.prefix = prefix
        self.score = 1
    
    def __str__(self):
        if self.prefix:
            return self.prefix
        return ''

    def insert(self, text):
        if len(text) < 1:
            return
        
        character = text[0]
        if character not in self.children:
            self.children[character] = TrieNode(self.prefix + character, character)
        else:
            self.children[character].score += 1
        
        self.children[character].insert(text[1:])

    
    def find_node(self, path):
        if len(path) < 1:
            return self

        character = path[0]

        if character == self.prefix:
            return self
        elif character in self.children:
            return self.children[character].find_node(path[1:])
        else:
            return None
 

    def get_sorted_children(self):
        result = []
        for char, node in self.children.items():
            result.append({"char": char, "score": node.score})
        result.sort(key=lambda item: item['score'], reverse=True)
        return result


    def get_all_titles(self):
        if len(self.children) < 1:
            yield {"title": self.prefix, "score":self.score}
        else:
            for node in self.children.values():
                for leaf in node.get_all_titles():
                    yield leaf

    def to_dict(self):
        if len(self.children) < 1:
            return self.__dict__
        children_dict = {}
        for c, node in self.children.items():
            children_dict[c] = node.to_dict()
        self.children = children_dict
        return self.__dict__
        