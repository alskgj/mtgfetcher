import cache


def most_relevant(data):
    # todo levenshtein distance? example with nicol bolas returning list of five
    return data[0]


def get_all(query):
    """Takes a query and returns the first 10 relevant datapoints"""
    data = cache.get(query)
    if not data:
        return []
    result = []
    for element in data:
        card = {}
        # todo both card faces
        if 'image_uris' not in element:
            element = element['card_faces'][0]

        card['png'] = element['image_uris']['png']
        card['thumbnail'] = element['image_uris']['small']
        card['name'] = element['name']
        card['id'] = element['id']
        result.append(card)
    return result


def get_image(query):
    """Takes a query and returns an uri
    to the most relevant magic card"""
    data = cache.get(query)
    if not data:
        return None
    return most_relevant(data)['image_uris']['png']
