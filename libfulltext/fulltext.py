from .elsevier import getElsevierFulltext
from .springer import getSpringerFulltext
from .crossref import getCrossrefMetadata

# metadata['message']['publisher'] = "American Physical Society (APS)"
#if 16 == metadata['message']['member']:
publisherHandler = {
        '78': (getElsevierFulltext,"elsevier"),
        '297': (getSpringerFulltext,"springer")
        }


def handleDoi(config, doi):
    # dois are case insensitive (wtf!)
    doi = doi.lower()

    metadata = getCrossrefMetadata(doi)

    try:
        crossRefMemberId = metadata['message']['member']
    except KeyError:
        # fixme: do this more nicely
        raise ValueError("There is no publisher data !!!! we're all gonna die")

    try:
        # publisher name to retrieve configuration from config file
        publisherGetter, publisherName = publisherHandler[crossRefMemberId]
    except KeyError:
        raise NotImplementedError(
                "getFulltext not implemented for member {}, "
                "publisher {}".format(
                    metadata['message']['member'],
                    metadata['message']['publisher']
                    )
                )

    return publisherGetter(metadata, config[publisherName])


prefixHandlers = {
    'doi': handleDoi,
}

def getFulltext(config, prefixedId):
    prefix, id = prefixedId.split(':', 1)
    try:
        handler = prefixHandlers[prefix]
    except KeyError:
        raise ValueError('Prefix {0} unknown.'.format(prefix))
    r = handler(config, id)
