"""DOI handler module"""

import requests

from .crossref import get_crossref_fulltext
from .datacite import get_datacite_fulltext

def get_doi_fulltext(config, doi):
    """Get fulltext for a DOI"""

    # dois are case insensitive (wtf!)
    doi = doi.lower()

    registration_agency = get_doi_registration_agency(doi)

    if registration_agency == 'Crossref':
        return get_crossref_fulltext(config, doi)
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
