import pandas
import os
from keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
import numpy as np

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

    return sequences, tokenizer.word_index

def train_test_generator( dataset, test_ratio = 0.2):
    return train_test_split(dataset, test_size = test_ratio, shuffle=True)

def prepare_data(file_name):
    # generate sequence of int from data
    data, word_index = sequences_preparation(file_name)
    # train test data split
    train, test = train_test_generator(data)
    train_features = []
    train_labels = []
    test_features = []
    test_labels = []
    for elem in train:
        train_features.append(elem[:-1])
        train_labels.append(elem[-1])
    for elem in test:
        test_features.append(elem[:-1])
        test_labels.append(elem[-1])

    train_label_one_hot = np.zeros((len(train_features), len(word_index) + 1), int)

    for ind, word_ind in enumerate(train_labels):
        train_label_one_hot[ind, word_ind] = 1
    return train_features, train_labels, test_features, test_labels, train_label_one_hot