import torch
import torch.nn.functional as F
from typing import Generator, Tuple

from .rnn import RNN
from .vectorize import concat_one_hot, devectorize, make_input_vect
from .config import FILEPATHS
from .preprocessor import preprocess_text, IX_TO_CHAR, CHAR_TO_IX, EOS, CATE_TO_IX


class ModelAdapter:
    def load(self):
        model_state = torch.load(FILEPATHS['model'], map_location=torch.device('cpu'))
        self.rnn = RNN(len(IX_TO_CHAR) + len(CATE_TO_IX), len(IX_TO_CHAR))
        if torch.cuda.is_available():
            self.rnn.cuda()
        self.rnn.load_state_dict(model_state)
        self.rnn.eval()
        return self

    def predict(self, prefix:str='', cate:str='-', top_n:int=20, max_length:int=100) -> list:

        title = preprocess_text(prefix)[:-1]
        X = make_input_vect(title, cate)
        
        with torch.no_grad():
            hidden = None
            for i in range(len(title) - 1):
                output, hidden = self.rnn.predict(X[-1].reshape(1, 1, -1), hidden)
            results = []
            for title_tensor, score in self._predict_helper(X, cate, hidden, top_n, max_length):
                new_title = {'title': devectorize(title_tensor), 'score': score}
                if new_title not in results:
                    results.append(new_title)            
            results.sort(key=lambda item: item['score'], reverse=True)
        return results[:top_n]

    def _predict_helper(self, X:torch.tensor, cate:str, hidden:torch.tensor=None, n:int=20, max_length:int=100, prefix_score:float=0) -> Generator[Tuple, None, None]:        
        score = prefix_score
        title_len = X.size()[0]
        
        for i in range(max_length - title_len):
            output, hidden = self.rnn.predict(X[-1].reshape(1, 1, -1), hidden)
            topv, topi = output.reshape(-1).topk(2)
            top_char_ix = topi[0].item()
            top_2_char_ix = topi[1].item()

            if n > 0 and top_2_char_ix != CHAR_TO_IX[EOS]:
                n = n // 2
                new_X = concat_one_hot(X, top_2_char_ix, cate)
                for result in self._predict_helper(new_X, cate, hidden, n, max_length, score + topv[1].item()):
                    yield result

            score += topv[0].item()
            if top_char_ix == CHAR_TO_IX[EOS]:
                break
            X = concat_one_hot(X, top_char_ix, cate)

        yield X[1:], score
