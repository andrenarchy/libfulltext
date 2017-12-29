"""Fulltext retrieval module"""

from .elsevier import get_elsevier_fulltext
from .springer import get_springer_fulltext
from .aps import get_aps_fulltext
from .crossref import get_crossref_metadata

PUBLISHER_HANDLERS = {
    '78': (get_elsevier_fulltext, "elsevier"),
    '297': (get_springer_fulltext, "springer"),
    '16': (get_aps_fulltext, "APS")
    }

def handle_doi(config, doi):
    """Handle a DOI"""
    # dois are case insensitive (wtf!)
    doi = doi.lower()

    metadata = get_crossref_metadata(doi)

    try:
        crossref_member_id = metadata['message']['member']
    except KeyError:
        # fixme: do this more nicely
        raise ValueError("There is no publisher data !!!! we're all gonna die")

    try:
        # publisher name to retrieve configuration from config file
        publisher_handler, publisher_name = PUBLISHER_HANDLERS[crossref_member_id]
    except KeyError:
        raise NotImplementedError(
            "getFulltext not implemented for member {}, "
            "publisher {}".format(
                metadata['message']['member'],
                metadata['message']['publisher']
                )
            )

    return publisher_handler(metadata, config[publisher_name])


PREFIX_HANDLERS = {
    'doi': handle_doi,
}

def get_fulltext(config, prefixed_identifier):
    """Get fulltext for a prefixed ID"""
    prefix, identifier = prefixed_identifier.split(':', 1)
    try:
        handler = PREFIX_HANDLERS[prefix]
    except KeyError:
        raise ValueError('Prefix {0} unknown.'.format(prefix))
    handler(config, identifier)
