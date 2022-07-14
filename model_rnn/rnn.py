import torch
import torch.nn as nn
import torch.nn.functional as F


class RNN(nn.Module):
    def __init__(self, input_size, output_size):
        super(RNN, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = 64
        self.rnn = nn.LSTM(input_size, self.hidden_size, batch_first=True)
        self.o2o = nn.Linear(self.hidden_size, output_size)
        self.dropout = nn.Dropout(0.1)

    def forward(self, input):
        # _, hidden = self.rnn(input)
        # out = self.o2o(hidden.reshape(-1, self.hidden_size))
        # out = self.dropout(out)
        output,_status = self.rnn(input)
        output = output[:,-1,:]
        output = self.o2o(torch.relu(output))
        output = self.dropout(output)
        return F.log_softmax(output, dim=1)

    def predict(self, input, hidden=None):
        output,_status = self.rnn(input)
        output = output[:,-1,:]
        output = self.o2o(torch.relu(output))
        output = self.dropout(output)
        return F.log_softmax(output, dim=1), hidden
