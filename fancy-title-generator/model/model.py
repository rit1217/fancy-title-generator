from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Masking, Embedding
import model.data_prep
import tensorflow as tf
import numpy as np
# from tensorflow.contrib import rnn
def train( data_file_name ):

    res = model.data_prep.prepare_data(data_file_name)

    train_features = res['train_features']
    train_labels = res['train_labels']
    test_features = res['test_features']
    test_labels = res['test_labels']
    num_words = res['num_words']

    training_model = Sequential()

    embedding_train = Embedding( input_dim=len(train_features), output_dim=16, mask_zero=True)
    train_features_embed = embedding_train(train_features)

    embedding_test = Embedding( input_dim=len(test_features), output_dim=16, mask_zero=True)
    test_features_embed = embedding_test(test_features)
    print(train_features_embed._keras_mask)
    print(test_features_embed._keras_mask)

    training_model.add(embedding_train)
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