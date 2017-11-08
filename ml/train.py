import numpy as np
import tflearn

def train_model(datapoints, user_id):
    X = datapoints.get('X')
    encoder = tflearn.input_data(shape=None)
    encoder = tflearn.fully_connected(encoder, 256)
    encoder = tflearn.fully_connected(encoder, 64)

    decoder = tflearn.fully_connected(encoder, 256)
    decoder = tflearn.fully_connected(decoder, 784, activation='sigmoid')

    net = tflearn.regression(decoder, optimier='adam', learning_rate=0.001,
                            loss='mean_square', metric=None)

    model = tflearn.DNN(net)

    model.fit(X, X, n_epoc=20, batch_size=256)

    encoding_model = tflearn.DNN(encoder, session = model.session)

    encoding_model.save('%s_trained_model.tflearn' % (user_id,))

    logging.debug("Successfully trained and saved model for user %s" % (
        user_id,
    ))

def predict(datapoint, user_id):
    
