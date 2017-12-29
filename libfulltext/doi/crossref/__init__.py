"""CrossRef DOI handler module"""

import requests

from .aps import get_aps_fulltext
from .elsevier import get_elsevier_fulltext
from .springer import get_springer_fulltext

def get_crossref_fulltext(config, doi):
    """Get fulltext for a CrossRef DOI"""

    metadata = get_crossref_metadata(doi)
    crossref_member = metadata['message']['member']

    if crossref_member == '16':
        return get_aps_fulltext(metadata)
    elif crossref_member == '78':
        return get_elsevier_fulltext(metadata, apikey=config['publishers']['elsevier']['apikey'])
    elif crossref_member == '297':
        return get_springer_fulltext(metadata)

    raise ValueError('No handler for DOI {0} (publisher {1}) found.'
                     .format(doi, metadata['message']['publisher']))

def get_crossref_metadata(doi):
    """Returns dict with CrossRef metadata for a DOI"""
    return requests.get('https://api.crossref.org/v1/works/' + doi).json()
