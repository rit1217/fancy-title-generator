from typing import Generator, NamedTuple, Optional


class TitleObj(NamedTuple):
    title: str
    score: int

    
class TrieNode:
    def __init__(self, char:str, score:int=1, children:dict[str, 'TrieNode']=None):
        self.children = children if children else {}
        self.char = char
        self.score = score

    def insert(self, text):
        if not text:
            return
        char = text[0]
        if char not in self.children:
            self.children[char] = TrieNode(char, 1, {})
        else:
            self.children[char].score += 1

        self.children[char].insert(text[1:])

    def find_node(self, path:str) -> Optional['TrieNode']:
        if not path:
            return self 
        elif path[0] not in self.children:
            return None
        return self.children.get(path[0]).find_node(path[1:])
 
    def get_all_titles(self, prefix:str) -> Generator[TitleObj, None, None]:
        if self.children:
            for char, node in self.children.items():
                for title_obj in node.get_all_titles(prefix + char):
                    yield title_obj
        else:
            yield TitleObj(title=prefix, score=self.score)

    def to_dict(self):
        children_dict = {}
        for char, node in self.children.items():
            children_dict[char] = node.to_dict()
        return {
            'char' : self.char,
            'score': self.score,
            'children': children_dict
        }