"""SpringerNature publisher module"""

import requests

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
    save_stream(response, 'fulltext.pdf')
