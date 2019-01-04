import requests
from json import loads, dumps
from os.path import exists

API = "https://api.scryfall.com/cards/search"
PATH = 'cache.json'


def search(query):
    """This returns a list of all matching cards. Can be an empty list."""
    response = requests.get(API, params={'q': query}).json()
    if response['object'] == 'error':
        return []
    else:
        return response['data']


def get(query):
    """Returns None if query isn't cached, else the data"""
    if not exists(PATH):
        return store(query)
    with open(PATH, 'r') as fo:
        data = loads(fo.read())
    if query in data:
        return data[query]
    else:
        return store(query)


def store(query):
    """Search query on scryfall, update db and return result"""
    result = search(query)

    if exists(PATH):
        data = loads(open(PATH, 'r').read())
        data[query] = result
    else:
        data = {query: result}

    with open(PATH, 'w') as fo:
        fo.write(dumps(data))
    return result
