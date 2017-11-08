import csv
import requests
from user import uid as user_uuid
from user import BASE_URL

# user_uuid = '36fe18b8-9795-40ac-94e5-63a88c838b63'
EXTENDED_URL = '%s/api/addTransaction' % BASE_URL


def get_data():
    with open('test_cases.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        data = []
        for row in reader:
            data.append(row)
    return data

def submit(data):
    for point in data:
        data = {
            'date_of_transaction': point[0],
            'amount': point[1],
            'details': point[2],
            'user_uuid': user_uuid}
        print(requests.post('http://127.0.0.1/api/addTransaction', json=data).content)

if __name__ == "__main__":
    submit(get_data())
