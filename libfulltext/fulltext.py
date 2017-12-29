"""Fulltext retrieval module"""

from .doi import get_doi_fulltext

PREFIX_HANDLERS = {
    'doi': get_doi_fulltext,
}


def get_fulltext(config, prefixed_identifier):
    """Get fulltext for a prefixed ID

    Args:
        config:               configuration dictionary
                              (see config.py and README.md)
        prefixed_identifier:  article identifier with prefix
                              (e.g. "doi:10.1016/j.cortex.2015.10.021")

    Raises:
        ValueError: Prefix is not implemented
    """
    prefix, identifier = prefixed_identifier.split(':', 1)
    try:
        handler = PREFIX_HANDLERS[prefix]
    except KeyError:
        raise ValueError('Prefix {0} unknown.'.format(prefix))
    handler(config, identifier)
