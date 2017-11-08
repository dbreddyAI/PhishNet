import nltk
from gensim.models import Word2Vec
import numpy as np

def _in_parse_model_file(user_id):
    return "ml/vectorize_models/%s_vectorize.gensim" % (user_id,)

def train_model(phrases, user_id):
    model = Word2Vec(phrases)
    # open(_in_parse_model_file(user_id), 'a').close()
    with open(_in_parse_model_file(user_id), 'w+') as f:
        pass
    model.save(_in_parse_model_file(user_id))

def vectorize(phrase, user_id):
    model = Word2Vec.load(_in_parse_model_file(user_id))
    return model.wv[phrase]

def multi_vectorize(phrases, user_id):
    model = Word2Vec.load(_in_parse_model_file(user_id))
    return [model.wv[x] for x in phrases]
