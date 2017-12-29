"""Fulltext retrieval module"""

from .aps import get_aps_fulltext
from .crossref import get_crossref_metadata
from .elsevier import get_elsevier_fulltext
from .springer import get_springer_fulltext

def handle_doi(config, doi):
    """Handle a DOI"""
    # dois are case insensitive (wtf!)
    doi = doi.lower()

    metadata = get_crossref_metadata(doi)
    crossref_member_id = metadata['message']['member']

    if crossref_member_id == '16':
        return get_aps_fulltext(metadata)
    elif crossref_member_id == '78':
        return get_elsevier_fulltext(metadata, apikey=config['publishers']['elsevier']['apikey'])
    elif crossref_member_id == '297':
        return get_springer_fulltext(metadata)

    raise ValueError('No handler for DOI {0} (publisher {1}) found.'
                     .format(doi, metadata['message']['publisher']))

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
