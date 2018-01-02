# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Elsevier publisher module"""

import requests

from ...utils import verify_response

def get_elsevier_fulltext(doi, save_stream, apikey):
    """Retrieve Elsevier fulltext

    Args:
        doi:         DOI string
        save_stream: function that saves a stream (arguments: stream, path)
        apikey:      Elsevier API key

    Raises:
        requests.exceptions.HTTPError: request was not successful
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

    verify_response(response, 'application/pdf')

    # Elsevier sometimes only returns the first page (yep, also for OA content)
    elsevier_status = response.headers['X-ELS-Status']
    if 'WARNING' in response.headers['X-ELS-Status']:
        raise requests.exceptions.HTTPError(
            'X-ELS-Status indicates that request was not successful: {0}'
            .format(elsevier_status)
            )

    save_stream(response, 'fulltext.pdf')
