class TrieNode:
    def __init__(self, word = None, parent = None):
        self.parent = parent
        self.children = {}
        self.word = word
        self.score = 1
    
    def __str__(self):
        if self.word:
            return self.word
        return ''

    def insert(self, text):
        if len(text) < 1:
            return
        
        word = text[0]
        if word not in self.children:
            if self.word:
                self.children[word] = TrieNode(self.word + ' ' + word, self)
            else:
                self.children[word] = TrieNode(word, self)
        else:
            self.children[word].score += 1
        
        self.children[word].insert(text[1:])

    
    def find(self, path):
        if len(path) < 1:
            return self

        word = path[0]
        if word == self.word:
            return self
        elif word in self.children:
            return self.children[word].find(path[1:])
        else:
            return None
 

    def suggest(self):
        result = []
        for word, node in self.children.items():
            result.append((word, node.score))
        result.sort(key=lambda item: item[1], reverse=True)
        return result

    def suggest_with_score_gen(self, prefix_path):
        if len(self.children) < 1:
            yield (self.word, self.score)
        else:
            for word, node in self.children.items():
                path = prefix_path
                path.append(word) 
                for leaf in node.suggest_with_score_gen(prefix_path):
                    yield leaf


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def add_data(self, new_suggestions):
        for suggestion in new_suggestions:
            self.root.insert(suggestion)

    def search(self, prefix):
        result = self.root.find(prefix)

        if result == None:
            return None
        
        return result.suggest()
    
    def print_suggestion(self, node, prefix):
 
        if len(node.children) < 1:
            print(prefix, node.score)
 
        for word, node in node.children.items():
            self.print_suggestion(node, prefix + ' ' + word)

    def autocomplete(self, prefix):
        cur_node = self.root
 
        for word in prefix:
            if word not in cur_node.children.keys():
                return 0
            cur_node = cur_node.children[word]
 
        
        if len(cur_node.children) < 1:
            return None

        # self.print_suggestion(cur_node, ' '.join(prefix))
        result = []
        for i in cur_node.suggest_with_score_gen(prefix):
            result.append(i)
        result.sort(key=lambda item: item[1], reverse=True)
        return result