"""Elsevier publisher module"""

import requests

def get_elsevier_fulltext(metadata, save_stream, apikey):
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
    save_stream(response, 'fulltext.pdf')
