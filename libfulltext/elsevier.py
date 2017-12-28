import requests


def getElsevierFulltext(metadata, config):
    """
    getElsevierFulltext

    Args:
        metadata: meta data dictionary about the DOI. Needs `metadata['message']['DOI']`
        config:   configuration for the corresponding publisher. Needs `config["apikey"]`
    """
    doi = metadata['message']['DOI']
    params = {
      'apiKey': config["apikey"],
      'httpAccept': 'application/pdf',
    }

    r = requests.get(
            'https://api.elsevier.com/content/article/doi/' + doi,
            params=params,
            stream=True
            )
    with open('/tmp/bla.pdf', 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
