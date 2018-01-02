# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""SpringerNature publisher module"""

import requests

from ...utils import verify_response

def get_springer_fulltext(doi, save_stream):
    """Retrieve SpringerNature fulltext

    Args:
        doi:         DOI string
        save_stream: function that saves a stream (arguments: stream, path)
    """
    response = requests.get(
        'https://link.springer.com/content/pdf/{0}.pdf'.format(doi),
        stream=True
        )

    verify_response(response, 'application/pdf')

    save_stream(response, 'fulltext.pdf')
