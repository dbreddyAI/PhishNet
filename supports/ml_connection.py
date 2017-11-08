import logging

import pandas as pd

from ml import outlier, supervised
from supports.database import Transactions, User
from supports.maps_api import get_distance
from supports import twil
# from supports import sendgrid_api
# import matplotlib.pyplot as plt

from server import db

base_headings = [
    'date_of_transction',
    'amount',
    'details',
    'uuid',
    'user_uuid',
    'location',
    'store_name'
]

def data_frame(query, columns):
    def make_row(x):
        return dict([(c, getattr(x, c)) for c in columns])
    return pd.DataFrame([make_row(x) for x in query])

def clean(df):
    cache = df
    rows = list(df)
    tbd = []
    num_rows = len(cache.index)
    for r in rows:
        if (df[r] == 0).sum() < 2:
            tbd.append(r)

    cache = cache.drop(tbd, axis=1)

    return cache

def transaction_to_df(trans, *missing_headers):
    df = data_frame(trans, base_headings)
    # df = pd.concat([df, pd.get_dummies(df['location'])], axis=1)
    # df = pd.concat([df, pd.get_dummies(df['store_name'])], axis=1)
    # df = df.drop(['location', 'store_name', 'uuid', 'user_uuid', 'details', 'date_of_transction', 'store_name'], axis=1)
    df = df.drop(['uuid', 'user_uuid', 'details', 'date_of_transction'], axis=1)
    # if missing_headers is not None:
    #    for h in missing_headers:
    #        df[h] = 0

    return df

def predict(transaction_id):
    transaction = Transactions.query.filter(Transactions.uuid == transaction_id).all()
    df = transaction_to_df(transaction)
    return outlier.predict(df, transaction[0].user_uuid)
'''
def initial_train(user_uuid):
    transactions = Transactions.query.filter(Transactions.user_uuid == user_uuid).all()
    df = transaction_to_df(transactions)
    headers = list(df)
    headers = [x for x in headers if x not in base_headings]

    outlier.train_model(df, user_uuid)
    print(df)
    dfs = [transaction_to_df([x], *headers) for x in transactions]
    # print(dfs)
    # return outlier.predict(dfs, user_uuid)
    return [
        outlier.predict(transaction_to_df([x], *headers), user_uuid) for x in transactions
    ]
'''
def initial_train(user_uuid):
    transactions = Transactions.query.filter(Transactions.user_uuid == user_uuid).all()
    user = User.query.filter(User.user_uuid == user_uuid).first()
    cache = transactions
    locations = []
    stores = []
    for t in range(len(cache)):
        if cache[t].location not in locations:
            cache[t].location = len(locations)
            locations.append(cache[t].location)
        else:
            cache[t].location = locations.index(cache[t].location)
        if cache[t].store_name not in stores:
            cache[t].store_name = len(stores)
            stores.append(cache[t].store_name)
        else:
            cache[t].store_name = stores.index(cache[t].store_name)
    df = transaction_to_df(cache)
    outlier.train_model(df, user_uuid)
    for x in range(len(transactions)):
        if outlier.predict(transaction_to_df([cache[x]]), user_uuid)[0] == -1:
            if transactions[x].fraud is None:
                transactions[x].fraud = True
                print("Sending out a notice via twillio to %s" % (user.phone))
                twil.notice('''
                    Warning! There was a possible fraudulant transaction detected on your account!
                ''', user.phone)
                db.session.commit()
    '''
    predictions = [
        outlier.predict(transaction_to_df([x]), user_uuid) for x in transactions
    ]
    '''
