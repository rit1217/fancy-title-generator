import time
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
import matplotlib.pyplot as plt
from ..rnn import RNN as Model
from ..dataset import Dataset
from ..config import FILEPATHS
from ..preprocessor import CHAR_TO_IX


def train():
    #Init data.
    torch.manual_seed(0)
    batch_size = 64
    dataset = Dataset()
    n_test = len(dataset) // 10
    dataset_train, dataset_test = random_split(dataset, (len(dataset) - n_test, n_test))
    assert len(dataset_test) >= batch_size, "Batch size should be reduced."
    dataloader_train = DataLoader(dataset_train,
        batch_size=batch_size, shuffle=True, drop_last=True, num_workers=0)
    dataloader_test = DataLoader(dataset_test,
        batch_size=batch_size, shuffle=False, drop_last=False, num_workers=0)

    #Init model.
    # model_config = torch.load(FILEPATHS['model'])

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model = Model(len(CHAR_TO_IX), len(CHAR_TO_IX)).to(device)
    # model.load_state_dict(model_config['state_dict'])

    loss_fn = nn.NLLLoss(reduction='mean')
    optim = torch.optim.Adam(model.parameters(), lr=0.0005)
    print(torch.cuda.is_available())
    print(torch.cuda.get_device_name(torch.cuda.current_device()))
    print(device)
    #Initial test.
    model.eval()
    losses = []
    with torch.no_grad():
        for X, y in dataloader_test:
            X, y = X.to(device), y.to(device)
            y_pred = model(X)
            loss = loss_fn(y_pred, y)
            assert torch.isfinite(loss)
            losses.append(loss)
    loss_init = torch.tensor(losses).mean().item()
    print(f'E0 TEST:{loss_init:.3f}')

    #Training
    loss_min = float('inf')
    max_unimproved_epochs, unimproved_epochs = 15, 0
    train_losses = []
    test_losses = []
    for epoch in range(1, 999):
        start_time = time.time()
        #Training.
        model.train()
        losses = []
        for X, y in dataloader_train:
            X, y = X.to(device), y.to(device)
            y_pred = model(X)
            loss = loss_fn(y_pred, y)
            assert torch.isfinite(loss)
            optim.zero_grad()
            loss.backward()
            optim.step()
            losses.append(loss.detach())
        loss_train = torch.tensor(losses).mean().item()
        train_losses.append(loss_train)
        #Testing.
        model.eval()
        losses = []
        with torch.no_grad():
            for X, y in dataloader_test:
                X, y = X.to(device), y.to(device)
                y_pred = model(X)
                loss = loss_fn(y_pred, y)
                assert torch.isfinite(loss)
                losses.append(loss.detach())
        loss_test = torch.tensor(losses).mean().item()
        test_losses.append(loss_test)
        #Feedback.
        print(f'E{epoch}'
            f' LOSS:{loss_train:.3f} {loss_test:.3f}'
            f' TOOK:{time.time() - start_time:.1f}s'
            f' UNIMPROVED:{unimproved_epochs} E')
        #Save state & early stopping.
        unimproved_epochs += 1
        if loss_test < loss_min:
            torch.save({'state_dict':model.state_dict(),
                        'params': {'input_size':model.input_size,
                                    'output_size':model.output_size}}
                        , FILEPATHS['model'])
            loss_min = loss_test
            unimproved_epochs = 0
        if unimproved_epochs > max_unimproved_epochs:
            print(f'E{epoch} Early stopping. BEST TEST:{loss_min:.5f}')
            plt.plot(train_losses)
            plt.show()
            plt.plot(test_losses)
            plt.show()
            break

    return loss_init, loss_min


