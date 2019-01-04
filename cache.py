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


def trim(searchresults):
    """Takes a list of cards from scryfall and trims most data to make caching a bit better"""
    result = []

    for element in searchresults:
        card = {}
        card['id'] = element['id']
        if 'image_uris' not in element:
            element = element['card_faces'][0]
        card['image_uris'] = {'small': element['image_uris']['small'], 'png': element['image_uris']['png']}
        card['name'] = element['name']
        result.append(card)
    return result


def store(query):
    """Search query on scryfall, update db and return result"""
    result = trim(search(query))

    if exists(PATH):
        data = loads(open(PATH, 'r').read())
        data[query] = result
    else:
        data = {query: result}

    with open(PATH, 'w') as fo:
        fo.write(dumps(data))
    return result
