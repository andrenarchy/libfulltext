"""DOI handler module"""

import requests

from .crossref import get_crossref_fulltext
from .datacite import get_datacite_fulltext

def get_doi_fulltext(config, doi, save_stream):
    """Get the fulltext for a DOI

    Args:
        config:      configuration dictionary (see config.py)
        doi:         DOI as string
        save_stream: function that saves a stream (arguments: stream, path)

    Raises:
        ValueError: Function to handle publisher is not implemented
    """

    # dois are case insensitive (wtf!)
    doi = doi.lower()

    registration_agency = get_doi_registration_agency(doi)

    if registration_agency == 'Crossref':
        return get_crossref_fulltext(config, doi, save_stream)
    elif registration_agency == 'DataCite':
        return get_datacite_fulltext()

    raise NotImplementedError('Registration agency {0} is not yet implemented.'
                              .format(registration_agency))


def get_doi_registration_agency(doi):
    """Get registration agency for a DOI"""
    ra_result = requests.get('https://doi.org/doiRA/' + doi).json()[0]
    if 'RA' not in ra_result:
        raise ValueError('No registration agency known for DOI {0}.'.format(doi))
    return ra_result['RA']
