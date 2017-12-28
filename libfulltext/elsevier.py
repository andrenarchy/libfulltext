import requests

def getElsevierFulltext(metadata, apiKey):
    doi = metadata['message']['DOI']
    params = {
      'apiKey': apiKey,
      'httpAccept': 'application/pdf',
    }

    r = requests.get('https://api.elsevier.com/content/article/doi/' + doi, params=params, stream=True)
    with open('/tmp/bla.pdf', 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
