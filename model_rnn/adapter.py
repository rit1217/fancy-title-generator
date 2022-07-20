import torch
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

    def predict(self, prefix:str='', max_length:int=100) -> list:
        score = 0
        with torch.no_grad():
            title = preprocess_text(prefix)[:-1]
            X = make_input_vect(title)
            hidden = None
            for i in range(len(title) - 1):
                output, hidden = self.rnn.predict(X[-1].reshape(1, 1, -1), hidden)
            for i in range(max_length - len(title)):
                output, hidden = self.rnn.predict(X[-1].reshape(1, 1, -1), hidden)
                topv, topi = output.reshape(-1).topk(1)
                score += topv[0].item()
                char = IX_TO_CHAR[topi[0].item()]
                if char == EOS:
                    break
                title += char
                X = make_input_vect(title)
            return [{'title':title[1:], 'score':score}]