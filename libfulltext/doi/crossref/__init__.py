# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""CrossRef DOI handler module"""

import requests

from .aps import get_aps_fulltext
from .elsevier import get_elsevier_fulltext
from .springer import get_springer_fulltext


def get_crossref_fulltext(doi, save_stream, config):
    """Get fulltext for a CrossRef doi

    Fetches metadata about a DOI from CrossRef to determine the publisher and
    pick the getter function accoridingly.

    Args:
        doi:           DOI as string
        save_stream:   a function with two arguments (data stream and output filename)
        config:        the libfulltext configuration dictionary

    Returns:
        What the actual getter returns (usually None)

    Raises:
        ValueError: no getter function for publisher found
    """

    metadata = get_crossref_metadata(doi)
    crossref_member = metadata['message']['member']

    if crossref_member == '16':
        return get_aps_fulltext(doi, save_stream)
    elif crossref_member == '78':
        return get_elsevier_fulltext(doi, save_stream,
                                     apikey=config['publishers_elsevier_apikey'])
    elif crossref_member == '297':
        return get_springer_fulltext(doi, save_stream)

    raise ValueError('No handler for DOI {0} (publisher {1}) found.'
                     .format(doi, metadata['message']['publisher']))


def get_crossref_metadata(doi):
    """Obtain metadata for DOI from crossref.org

    Args:
        doi: DOI as string

    Returns:
        dict with CrossRef metadata
    """
    response = requests.get('https://api.crossref.org/v1/works/' + doi)
    response.raise_for_status()
    return response.json()
