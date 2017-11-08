import requests

BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'

def get_distance(locationA, locationB):
    request = requests.get(BASE_URL, params = {
        'units': 'metric',
        'origins': locationA,
        'destinations': locationB,
        'key': 'AIzaSyAJZnzR9qlj8fIPi1bn2RsUuu2gFy_w6OQ'
    })

    if request.status_code == requests.codes.OK:
        data = request.json()
        distance = data['rows'][0]['elements'][0]['distance']['value']
        return distance

    return None
