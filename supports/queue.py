from supports import ml_connection as ml

from redis import Redis
from rq import Queue

q = Queue(connection=Redis())

def initial_train(user_uuid):
    ml.initial_train(user_uuid)

def queue_initial_train(user_uuid):
    result = q.enqueue(
        initial_train,
        user_uuid)
