import requests

def getCrossrefMetadata(doi):
    return requests.get('https://api.crossref.org/v1/works/' + doi).json()
