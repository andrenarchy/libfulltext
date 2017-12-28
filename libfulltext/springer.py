import requests


def getSpringerFulltext(metadata, config):
    doi = metadata['message']['DOI']

    r = requests.get(
            'https://link.springer.com/content/pdf/{0}.pdf'.format(doi) + doi,
            stream=True
            )
    with open('/tmp/bla.pdf', 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
