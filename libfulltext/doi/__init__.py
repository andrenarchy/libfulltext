# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""DOI handler module"""

import requests

from .crossref import get_crossref_fulltext
from .datacite import get_datacite_fulltext


def get_doi_fulltext(doi, save_stream, config):
    """Get the fulltext for a DOI

    Args:
        doi:         DOI string
        save_stream: function that saves a stream (arguments: stream, path)
        config:      configuration dictionary (see config.py)

    Returns:
        What the actual getter returns (usually None)

    Raises:
        NotImplementedError: Function to handle publisher is not implemented
    """

    # dois are case insensitive (wtf!)
    doi = doi.lower()

    registration_agency = get_doi_registration_agency(doi)

    if registration_agency == 'Crossref':
        return get_crossref_fulltext(doi, save_stream, config)
    elif registration_agency == 'DataCite':
        return get_datacite_fulltext()

    raise NotImplementedError('Registration agency {0} is not yet implemented.'
                              .format(registration_agency))


def get_doi_registration_agency(doi):
    """Get registration agency for a DOI

    Args:
        doi: the DOI as a string

    Returns:
        registration agency as a string

    Raises:
        ValueError: registration agency not known to doi.org
    """

    response = requests.get('https://doi.org/doiRA/' + doi)
    response.raise_for_status()
    ra_result = response.json()[0]
    if 'RA' not in ra_result:
        raise ValueError('No registration agency known for DOI {0}.'.format(doi))
    return ra_result['RA']
