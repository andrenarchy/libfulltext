"""SpringerNature publisher module"""

import requests
from ...stream import save_to_file

def get_springer_fulltext(metadata):
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
    save_to_file(response)
