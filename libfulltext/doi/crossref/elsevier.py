"""Elsevier publisher module"""

import requests

def get_elsevier_fulltext(doi, save_stream, apikey):
    """Retrieve Elsevier fulltext

    Args:
        doi:         DOI string
        save_stream: function that saves a stream (arguments: stream, path)
        apikey:      Elsevier API key
    """
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
