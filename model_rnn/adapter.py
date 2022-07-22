import torch
from typing import Generator, Dict
from .rnn import RNN
from .vectorize import make_input_vect
from .config import FILEPATHS
from .preprocessor import preprocess_text, IX_TO_CHAR, EOS


class ModelAdapter:
    def load(self):
        model_state = torch.load(FILEPATHS['model'], map_location=torch.device('cpu'))
        self.rnn = RNN(len(IX_TO_CHAR), len(IX_TO_CHAR))
        if torch.cuda.is_available():
            self.rnn.cuda()
        self.rnn.load_state_dict(model_state)
        self.rnn.eval()
        return self

    def predict(self, prefix:str='', top_n:int=20, max_length:int=100) -> list:
        title = preprocess_text(prefix)[:-1]
        result = []
        for res in self._predict_helper(title, top_n, max_length):
            result.append(res)
        result.sort(key=lambda item: item['score'], reverse=True)
        return result[:top_n]

    def _predict_helper(self, title:str, n:int=20, max_length:int=100, prefix_score:float=0) -> Generator[Dict, None, None]:        
        score = prefix_score
        with torch.no_grad():
            X = make_input_vect(title)
            hidden = None
            for i in range(len(title) - 1):
                output, hidden = self.rnn.predict(X[-1].reshape(1, 1, -1), hidden)
            for i in range(max_length - len(title)):
                output, hidden = self.rnn.predict(X[-1].reshape(1, 1, -1), hidden)
                topv, topi = output.reshape(-1).topk(2)
                top_char = IX_TO_CHAR[topi[0].item()]
                top_2_char = IX_TO_CHAR[topi[1].item()]

                if n > 0 and top_2_char != EOS:
                    n = n // 2
                    for result in self._predict_helper(title + top_2_char, n, max_length, score + topv[1].item()):
                        yield result

                score += topv[0].item()
                if top_char == EOS:
                    break
                title += top_char
                X = make_input_vect(title)

            yield {'title':title[1:], 'score':score}
