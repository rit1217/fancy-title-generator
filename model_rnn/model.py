import torch
from .rnn import RNN
from .vectorize import make_input_vect
from .config import FILEPATHS
from .config import BOS, EOS, DATA_IX_TO_CHAR


class RNNModel:
    def load(self):
        model_config = torch.load(FILEPATHS['model'])
        params = model_config['params']
        self.rnn = RNN(params['input_size'],params['output_size'])
        if torch.cuda.is_available():
            self.rnn.cuda()
        self.rnn.load_state_dict(model_config['state_dict'])
        self.rnn.eval()
        return self

    def predict(self, prefix:str='', max_length:int=25) -> list:
        with torch.no_grad():
            title = BOS + prefix
            X = make_input_vect(title)
            hidden = None
            for i in range(len(title) - 1):
                output, hidden = self.rnn.predict(X[i].reshape(1, 1, -1), hidden)
            for i in range(max_length - len(title)):
                output, hidden = self.rnn.predict(X[-1].reshape(1, 1, -1), hidden)
                topv, topi = output.reshape(-1).topk(1)
                char = DATA_IX_TO_CHAR[topi[0].item()]
                if char == EOS:
                    break
                title += char
                X = make_input_vect(title)
            return title[1:]