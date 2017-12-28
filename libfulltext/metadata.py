import requests

def getCrossrefMetadata(doi):
    r = requests.get('https://api.crossref.org/v1/works/' + doi)
    return r.json()
