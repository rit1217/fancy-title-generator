import graph_model.trie_model as trie_model
import json
class GraphModel:
    def __init__(self):
        self.trie = trie_model.Trie()

    def train(self):
        try:
            data_file = open('./temp/data/pre_proceed_data.txt', 'r')
        except:
            trie_model.data_preprocess()
            data_file = open('./temp/data/pre_proceed_data.txt', 'r')

        content = data_file.read().splitlines()
        data_file.close()
        data_list = []
        for line in content:
            data_list.append(line)

        self.trie.add_data(data_list)
        return self

    def load(self):
        with open('./temp/model.json', 'rt') as f:
            json_data = json.load(f)
        self.trie.load(json_data)
        return self

    def save(self):
        with open('./temp/model.json', 'wt') as f:
            json.dump(self.trie.to_dict(), f)

    def predict(self, prefix, top_n):
        return self.trie.autocomplete( prefix, top_n)
        