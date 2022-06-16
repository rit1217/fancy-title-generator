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
                self.children[word] = TrieNode(self.word + word, self)
            else:
                self.children[word] = TrieNode(word, self)
        else:
            self.children[word].score += 1
        
        self.children[word].insert(text[1:])

    
    def find(self, path):
        if len(path) < 1:
            return self

        word = path[0]
        print('path:', path, word, self.children, self.word)

        if word == self.word:
            return self
        elif word in self.children:
            return self.children[word].find(path[1:])
        else:
            return None
 

    def suggest(self):
        result = []
        for word, node in self.children.items():
            result.append({"word": word, "score": node.score})
        result.sort(key=lambda item: item['score'], reverse=True)
        return result

    def suggest_with_score_gen(self, prefix_path):
        if len(self.children) < 1:
            yield {"word": self.word, "score":self.score}
        else:
            for word, node in self.children.items():
                path = prefix_path + word
                # path.append(word) 
                for leaf in node.suggest_with_score_gen(prefix_path):
                    yield leaf

    def all_words(self, prefix_path):
        if len(self.children) < 1:
            yield {"word": self.word, "score":self.score}
        else:
            for word, node in self.children.items():
                path = prefix_path + word
                # path.append(word) 
                if word != ' ':
                    for leaf in node.suggest_with_score_gen(prefix_path):
                        yield {'word':prefix_path + leaf['word'], 'score':leaf['score']}