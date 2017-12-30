"""American Physical Society publisher module"""

import requests

def get_aps_fulltext(metadata, save_stream):
    """Retrieve APS fulltext

    Args:
        metadata:    CrossRef metadata dict
        save_stream: function that saves a stream (arguments: stream, path)
    """
    doi = metadata['message']['DOI']

    response = requests.get(
        'http://harvest.aps.org/v2/journals/articles/{0}'.format(doi),
        headers={"Accept": "application/pdf"},
        stream=True
        )
    save_stream(response, 'fulltext.pdf')
