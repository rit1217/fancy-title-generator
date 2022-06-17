from numpy import char

class TrieNode:
    def __init__(self, prefix = '', char = '', parent = None):
        self.parent = parent
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
            self.children[character] = TrieNode(self.prefix + character, character, self)
        else:
            self.children[character].score += 1
        
        self.children[character].insert(text[1:])

    
    def find_leaf(self, path):
        if len(path) < 1:
            return self

        character = path[0]
        print('path:', path, character, self.children, self.prefix)

        if character == self.prefix:
            return self
        elif character in self.children:
            return self.children[character].find(path[1:])
        else:
            return None
 

    def get_sorted_children(self):
        result = []
        for char, node in self.children.items():
            result.append({"char": char, "score": node.score})
        result.sort(key=lambda item: item['score'], reverse=True)
        return result


    def suggest_whole_title(self, prefix_path):
        # beam_size = 2
        if len(self.children) < 1:
            yield {"word": self.prefix, "score":self.score}
        else:
            # temp = list(self.children.values())
            # temp.sort(key=lambda item: item.score, reverse=True)          
            # for i in range(beam_size):
            #     if i < len(temp):
            #         for leaf in temp[i].suggest_whole_title(prefix_path):
            #             yield leaf
            for char, node in self.children.items():
                # path = prefix_path + word
                # path.append(word) 
                for leaf in node.suggest_whole_title(prefix_path):
                    yield leaf

    def all_titles(self, prefix_path):
        if len(self.children) < 1:
            yield {"word": self.prefix, "score":self.score}
        else:
            for word, node in self.children.items():
                path = prefix_path + word
                # path.append(word) 
                if word != ' ':
                    for leaf in node.suggest_whole_title(prefix_path):
                        yield {'word':prefix_path + leaf['word'], 'score':leaf['score']}