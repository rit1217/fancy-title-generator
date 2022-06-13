import pandas
import os
from keras.preprocessing.text import Tokenizer


def sequences_preparation(file_name):
    # read data from file
    data_file = open(file_name, 'r')
    contents = data_file.readlines()
    contents = contents[1:] # remove header
    product_labels = []

    # tokenize the product titles
    for line in contents:
        temp = "".join(line.split(',')[9:])
        product_labels.append(temp)

    # initialize keras Tokenizer
    tokenizer = Tokenizer(num_words = None, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                lower=True, split=' ')
    # train tokenizer to texts
    tokenizer.fit_on_texts(product_labels)

    # convert string to sequence of ints
    sequences = tokenizer.texts_to_sequences(product_labels)

    return sequences

data = sequences_preparation('data/fashionMNIST.csv')

for i in data[6040:6050]:
    print(i)
