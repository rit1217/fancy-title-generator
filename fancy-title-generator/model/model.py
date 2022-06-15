from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Masking, Embedding
import model.data_prep
import tensorflow as tf
import numpy as np
# from tensorflow.contrib import rnn
def train( data_file_name ):

    res = model.data_prep.prepare_data(data_file_name)

    train_features = res['train_features']
    train_features = tf.keras.preprocessing.sequence.pad_sequences(train_features, padding='post')
    train_labels = res['train_labels']
    test_features = res['test_features']
    test_features = tf.keras.preprocessing.sequence.pad_sequences(test_features, padding='post')
    print( '######', len(train_features[0]), len(test_features[0]))
    test_labels = res['test_labels']
    num_words = res['num_words']

    # print(num_words)
    # print()
    # print(train_features[:10])
    # print(train_labels[:10])
    # print(np.reshape(train_features[:10], [-1,]))
    # print()
    # print( type(train_features), type(train_features[0]), train_labels[0])
    # print()

    # # params
    # learning_rate = 0.001
    # iterations = 1000
    # n_input = 2

    # n_hidden = 512

    # # tensorflow graph input
    # x = tf.placeholder("float", [None, n_input, 1])
    # y = tf.placeholder("float", [None, num_words])

    # # output node weights and biases
    # weights = { 'out': tf.Variable(tf.random_normal([n_hidden, num_words]))}
    # biases = {'out': tf.Variable(tf.random_normal([num_words]))}

    # def RNN(var_x, w, b):
    #     var_x = tf.reshape(var_x, [-1, n_input])
    #     var_x = tf.split(var_x, n_input, 1)

    #     rnn_cell = rnn.MultiRNNCell([rnn.BasicLSTMCell(n_hidden), rnn.BasicLSTMCell(n_hidden)])

    #     outputs, states = rnn.static_rnn( rnn_cell, var_x, dtype=tf.float32)

    #     return tf.matmul(outputs[-1], weights['out'] + biases['out'])

    # pred = RNN(x, weights, biases)

    # cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
    # optimizer = tf.train.RMSPropOptimizer(learning_rate=learning_rate).minimize(cost)

    # correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    # init = tf.global_variables_intializer()


    training_model = Sequential()

    embedding = Embedding( input_dim=len(train_features), output_dim=16, mask_zero=True)
    train_features_embed = embedding(train_features)

    embedding_test = Embedding( input_dim=len(test_features), output_dim=16, mask_zero=True)
    test_features_embed = embedding_test(test_features)
    print(train_features_embed._keras_mask)
    print(test_features_embed._keras_mask)

    training_model.add(embedding)
    # # Embedding layer
    # training_model.add(
        # Embedding(input_dim=len(train_features),
        #         output_dim=100,
        #         weights=None,
        #         trainable=True,
        #         mask_zero=True))

    training_model.add(Masking())

    # Recurrent layer
    training_model.add(LSTM(64, return_sequences=False, 
                dropout=0.1, recurrent_dropout=0.1, input_shape=(len(train_features), len(train_features[0]))))

    # Fully connected layer
    training_model.add(Dense(64, activation='relu'))

    # Dropout for regularization
    training_model.add(Dropout(0.5))

    # Output layer
    training_model.add(Dense(num_words, activation='softmax'))

    # Compile the model
    training_model.compile( optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    # training_model.build(input_shape=(len(train_features), len(train_features[0])))
    training_model.summary()
    
    # ts1 = tf.convert_to_tensor(train_features, dtype=np.int64, name='ts1')
    # ts2 = tf.convert_to_tensor(train_labels_one_hot, dtype=int, name='ts2')

    # print(ts1)
    # train
    history = training_model.fit(train_features,  train_labels, 
                        batch_size=2048, epochs=500,
                        validation_data=(test_features, test_labels))
    training_model.save('trained_models')
    return history