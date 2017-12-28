import requests

from .elsevier import getElsevierFulltext
from .crossref import getCrossrefMetadata

def handleDoi(config, doi):
    # dois are case insensitive (wtf!)
    doi = doi.lower()

    metadata = getCrossrefMetadata(doi)

    # TODO: publisher switch

    return getElsevierFulltext(metadata, apiKey=config['elsevierApiKey'])

prefixHandlers = {
    'doi': handleDoi,
}

def getFulltext(config, prefixedId):
    prefix, id = prefixedId.split(':', 1)
    try:
        handler = prefixHandlers[prefix]
    except KeyError:
        raise ValueError('Prefix {0} unknown.'.format(prefix))
    r = handler(config, id)
