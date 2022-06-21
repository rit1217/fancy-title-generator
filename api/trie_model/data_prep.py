import pandas as pd
import os
import keras.preprocessing.text as keras_text_prep
import sklearn.model_selection
import numpy as np
import tensorflow as tf

filters='!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n'

# for fashionData2.csv only
def data2_preparation(file_name):
    df = pd.read_csv(file_name, quotechar='"')
    print(f"Data 2 has {len(df)} rows")
    return remove_punctuation(df['title'].values)

# for fashionProducts.csv only
def data1_preparation(file_name):
    # read data from file
    data_file = open(file_name, 'r')
    contents = data_file.readlines()
    contents = contents[1:] # remove header
    product_labels = []

    # tokenize the product titles
    for line in contents:
        temp = "".join(line.split(',')[9:])
        product_labels.append(temp)
    product_labels = remove_punctuation(product_labels)
    return product_labels


# remove unconsider characters from words in the sequence
def remove_punctuation(word_sequences):
    sequence_labels = []    
    for word in word_sequences:
        
        sequence_labels.append(' '.join(tf.keras.preprocessing.text.text_to_word_sequence(
                        word,
                        filters='!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n',
                        lower=True,
                        split=' '
                        )))
    return sequence_labels


## ------- OLD RNN APPROACH ------

# split input string into sequence of words
def input_split(in_string):
    return  tf.keras.preprocessing.text.text_to_word_sequence(
                        in_string,
                        filters='!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n',
                        lower=True,
                        split=' '
                        )

# convert list of string into list of seqeunces of words
def sequences_preparation(product_labels):
    # initialize keras Tokenizer
    tokenizer = keras_text_prep.Tokenizer(num_words = None, filters='!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n',
                lower=True, split=' ')
    # train tokenizer to texts
    tokenizer.fit_on_texts(product_labels)

    # convert string to sequence of ints
    sequences = tokenizer.texts_to_sequences(product_labels)
    return sequences, tokenizer.word_index


# split train and test data
def train_test_generator( dataset, test_ratio = 0.2):
    return sklearn.model_selection.train_test_split(dataset, test_size = test_ratio, shuffle=True)

# prepare data for RNN training
def prepare_data(file_name):
    data = data1_preparation(file_name)
    # generate sequence of int from data
    data, word_index = sequences_preparation(file_name)
    # train test data split
    train, test = train_test_generator(data)
    train_features = []
    train_labels = []
    test_features = []
    test_labels = []
    for elem in train:
        # train_features.append(np.array(elem[:-1]))
        train_features.append(elem[:-1])
        train_labels.append(elem[-1])
    for elem in test:
        # test_features.append(np.array(elem[:-1]))
        test_features.append(elem[:-1])
        test_labels.append(elem[-1])

    num_words = len(word_index) + 1
    train_label_one_hot = np.zeros((len(train_features), num_words), np.int8)
    test_label_one_hot = np.zeros((len(test_features), num_words), np.int8)

    for ind, word_ind in enumerate(train_labels):
        train_label_one_hot[ind, word_ind] = 1
    for ind, word_ind in enumerate(test_labels):
        test_label_one_hot[ind, word_ind] = 1
        
    
    train_features = tf.keras.preprocessing.sequence.pad_sequences(np.array(train_features), padding='post')
    test_features = tf.keras.preprocessing.sequence.pad_sequences(np.array(test_features), padding='post')

    result = {'train_features':train_features,
            'train_labels': train_label_one_hot,
            'test_features': test_features,
            'test_labels':test_label_one_hot,
            'num_words': num_words}
    return result
