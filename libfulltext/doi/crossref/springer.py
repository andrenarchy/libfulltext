"""SpringerNature publisher module"""

import requests

def get_springer_fulltext(metadata, save_stream):
    """Retrieve SpringerNature fulltext

    Args:
        metadata:    CrossRef metadata dict
        save_stream: function that saves a stream (arguments: stream, path)
    """
    doi = metadata['message']['DOI']

    response = requests.get(
        'https://link.springer.com/content/pdf/{0}.pdf'.format(doi),
        stream=True
        )
    save_stream(response, 'fulltext.pdf')
