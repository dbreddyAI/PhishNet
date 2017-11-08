import numpy as np
from sklearn.neighbors import KNeighborsClassifier

def train(datapoints, user_id):
    classifier = KNeighborsClassifier()
    classifier.fit(
        datapoints.get('points'),
        datapoints.get('fraud'))
    pickle.dump(
        classifier,
        open("supervised_models/%s_model.sklearn" % (user_id,), "rb")
    )

def predict(datapoint, user_id):
    classifier = pickle.load(
        open("supervised_models/%s_model.sklearn" % (user_id,), "r"))
    return classifier.predict(datapoint)
