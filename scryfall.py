import requests

API = "https://api.scryfall.com/cards/search"


def search(query):
    """This returns a list of all matching cards. Can be an empty list."""
    response = requests.get(API, params={'q': query}).json()
    if response['object'] == 'error':
        return []
    else:
        return response['data']


def most_relevant(data):
    # todo levenshtein distance? example with nicol bolas returning list of five
    return data[0]


def get_all(query):
    """Takes a query and returns all relevant datapoints"""
    data = search(query)
    if not data:
        return []
    result = []
    for element in data:
        card = {}
        # todo both card faces
        if 'image_uris' not in element:
            element = element['card_faces'][0]

        card['png'] = element['image_uris']['png']
        card['name'] = element['name']
        result.append(card)
    return result


def get_image(query):
    """Takes a query and returns an uri
    to the most relevant magic card"""
    data = search(query)
    if not data:
        return None
    return most_relevant(data)['image_uris']['png']


print(get_all('nicol bolas'))