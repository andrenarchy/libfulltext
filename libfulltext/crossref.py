"""CrossRef metadata module"""

import requests

def get_crossref_metadata(doi):
    """Returns dict with CrossRef metadata for a DOI"""
    return requests.get('https://api.crossref.org/v1/works/' + doi).json()
