"""SpringerNature publisher module"""

import requests

def get_springer_fulltext(metadata, save_stream):
    """Retrieve SpringerNature fulltext

    Args:
        metadata: meta data dictionary about the DOI. Needs `metadata['message']['DOI']`
        config:   configuration for the corresponding publisher (ignored)
    """
    doi = metadata['message']['DOI']

    response = requests.get(
        'https://link.springer.com/content/pdf/{0}.pdf'.format(doi),
        stream=True
        )
    save_stream(response, 'fulltext.pdf')
