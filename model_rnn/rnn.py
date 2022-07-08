import torch.nn as nn
import torch.nn.functional as F


class RNN(nn.Module):
    def __init__(self, input_size, output_size):
        super(RNN, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = 64
        self.rnn = nn.RNN(input_size, self.hidden_size, batch_first=True)
        self.o2o = nn.Linear(self.hidden_size, output_size)
        self.dropout = nn.Dropout(0.1)

    def forward(self, input):
        _, hidden = self.rnn(input)
        out = self.o2o(hidden.reshape(-1, self.hidden_size))
        out = self.dropout(out)
        return F.log_softmax(out, dim=1)

    def predict(self, input, hidden=None):
        _, hidden = self.rnn(input, hidden)
        out = self.o2o(hidden.reshape(-1, self.hidden_size))
        out = self.dropout(out)
        return F.log_softmax(out, dim=1), hidden
