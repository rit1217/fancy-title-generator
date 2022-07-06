import torch
import torch.nn as nn
import time
from .rnn import RNN
from .dataset import Dataset
from .scripts import make_input_vect
from .config import MODEL_FILEPATH, MODEL_STOP_EPOCH, MODEL_MAX_TRAIN_EPOCH
from .config import DATA_CHAR_START, DATA_CHAR_END, DATA_IX_TO_CHAR, DATA_CHAR_TO_IX


class RNNModel:
    def train(self, data:Dataset):
        batch_size = len(data.X)
        input_size = len(DATA_CHAR_TO_IX)
        output_size = len(DATA_CHAR_TO_IX)
        hidden_size = 64
        self.rnn = RNN(batch_size, input_size, hidden_size, output_size)
        if torch.cuda.is_available():
            self.rnn.cuda()
        loss_fn = nn.NLLLoss(reduction='mean')
        optimizer = torch.optim.Adam(self.rnn.parameters(), lr=0.01) 

        unimproved_epochs = 0
        loss_min = float('inf')
        start_time = time.time()

        for epoch in range(MODEL_MAX_TRAIN_EPOCH):
            #Training.
            self.rnn.train()
            y_pred = self.rnn(data.Z)
            loss = loss_fn(y_pred, data.y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            loss_train = loss.item()
            #Testing.
            self.rnn.eval()
            y_pred = self.rnn(data.Zt)
            loss_test = loss_fn(y_pred, data.yt).item()
            #Feedback.
            print(f'Epoch: {epoch} TRAIN: {loss_train:.3f} TEST: {loss_test:.3f}')
            #Early stopping.
            unimproved_epochs += 1
            if loss_test < loss_min:
                torch.save(self.rnn.state_dict(), MODEL_FILEPATH)
                loss_min = loss_test
                unimproved_epochs = 0
            if unimproved_epochs > MODEL_STOP_EPOCH:
                minutes_took = (time.time() - start_time) / 60
                print(f'E {epoch} Early stopping. BEST TEST: {loss_min:.3f}')
                print(f'Took: {minutes_took:.1f}m')
                break
        return self

    def load(self):
        model_config = torch.load(MODEL_FILEPATH)
        params = model_config['params']
        self.rnn = RNN(params['batch_size'],params['input_size'],params['hidden_size'],params['output_size'])
        if torch.cuda.is_available():
            self.rnn.cuda()
        self.rnn.load_state_dict(model_config['state_dict'])
        self.rnn.eval()
        return self

    def save(self):
        torch.save({'state_dict': self.rnn.state_dict(),
                    'params': {'batch_size': self.rnn.batch_size, 
                                'input_size': self.rnn.input_size,
                                'hidden_size': self.rnn.hidden_size,
                                'output_size': self.rnn.output_size}},
                    MODEL_FILEPATH)

    def predict(self, prefix:str='', max_length:int=20) -> list:
        with torch.no_grad():
            title = DATA_CHAR_START + prefix
            X = make_input_vect(title)
            hidden = None
            for i in range(len(title) - 1):
                output, hidden = self.rnn.predict(X[i].reshape(1, 1, -1), hidden)
            for i in range(max_length - len(title)):
                output, hidden = self.rnn.predict(X[-1].reshape(1, 1, -1), hidden)
                topv, topi = output.reshape(-1).topk(1)
                char = DATA_IX_TO_CHAR[topi[0].item()]
                if char == DATA_CHAR_END:
                    break
                title += char
                X = make_input_vect(title)
            return title[1:]