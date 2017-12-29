"""Fulltext retrieval module"""

from .doi import get_doi_fulltext

PREFIX_HANDLERS = {
    'doi': get_doi_fulltext,
}

def get_fulltext(config, prefixed_identifier):
    """Get fulltext for a prefixed ID"""
    prefix, identifier = prefixed_identifier.split(':', 1)
    try:
        handler = PREFIX_HANDLERS[prefix]
    except KeyError:
        raise ValueError('Prefix {0} unknown.'.format(prefix))
    handler(config, identifier)
