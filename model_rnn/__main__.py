from .model import RNNModel as Model
from .dataset import Dataset


data = Dataset()
Model().train(data).save()