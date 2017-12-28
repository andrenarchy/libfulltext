import requests


def getAPSFulltext(metadata, config):
    doi = metadata['message']['DOI']

    r = requests.get(
            'http://harvest.aps.org/v2/journals/articles/{0}'.format(doi),
            headers={"Accept": "application/pdf"},
            stream=True
            )
    with open('/tmp/bla.pdf', 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
