import requests
from user import uid as user_uuid
from user import BASE_URL
ADD_URL = '%s/api/addTransaction' % BASE_URL

data = {
    'date_of_transaction': 'Dec 31, 2018',
    'amount': '10.1',
    'details': 'Canadian Tire Ottawa, ON',
    'user_uuid': user_uuid,
}

def send():
    return requests.post(ADD_URL, json=data)
