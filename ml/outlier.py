import pickle

import numpy as np
from sklearn import svm
from sklearn.ensemble import IsolationForest

def train_model(datapoints, user_id):
    num_samples = 100
    outliers_frac = .01
    classifier = IsolationForest(
        max_samples=num_samples,
        contamination=outliers_frac
    )

    classifier.fit(datapoints)

    pickle.dump(classifier, open("ml/outlier_models/%s_model.sklearn" % (user_id,), "wb"))

def predict(datapoint, user_id):
    classifier = pickle.load(open("ml/outlier_models/%s_model.sklearn" % (user_id,), "rb"))
    return classifier.predict(datapoint)
