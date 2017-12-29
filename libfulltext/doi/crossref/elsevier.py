"""Elsevier publisher module"""

import requests
from ...stream import save_to_file

def get_elsevier_fulltext(metadata, apikey):
    """Retrieve Elsevier fulltext

    Args:
        metadata: meta data dictionary about the DOI. Needs `metadata['message']['DOI']`
        config:   configuration for the corresponding publisher. Needs `config["apikey"]`
    """
    doi = metadata['message']['DOI']
    params = {
        'apiKey': apikey,
        'httpAccept': 'application/pdf',
    }

    response = requests.get(
        'https://api.elsevier.com/content/article/doi/' + doi,
        params=params,
        stream=True
        )
    save_to_file(response)
