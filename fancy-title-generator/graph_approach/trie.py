from graph_approach.trie_node import TrieNode
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def add_data(self, new_suggestions):
        for suggestion in new_suggestions:
            self.root.insert(suggestion)

    def search(self, prefix):
        result = self.root.find(prefix)

        if result == None:
            return []
        
        return result.suggest(prefix)
    
    def print_suggestion(self, node, prefix):
 
        if len(node.children) < 1:
            print(prefix, node.score)
 
        for word, node in node.children.items():
            self.print_suggestion(node, prefix + word)

    def autocomplete(self, prefix):
        cur_node = self.root
 
        for word in prefix:
            if word not in cur_node.children.keys():
                return []
            cur_node = cur_node.children[word]
 
        
        if len(cur_node.children) < 1:
            return []

        # self.print_suggestion(cur_node, ' '.join(prefix))
        result = []
        for i in cur_node.suggest_with_score_gen(prefix):
            result.append(i)
        result.sort(key=lambda item: item['score'], reverse=True)
        return result