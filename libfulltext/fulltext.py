"""Fulltext retrieval module"""

import os

from .doi import get_doi_fulltext

PREFIX_FULLTEXT_GETTER = {
    'doi': get_doi_fulltext,
}

def get_fulltext(prefixed_identifier, fulltext_dirname, config):
    """Get fulltext for a prefixed ID

    Args:
        prefixed_identifier:  article identifier with prefix
                              (e.g. "doi:10.1016/j.cortex.2015.10.021")
        fulltext_dirname:     name of root directory for fulltext documents
        config:               configuration dictionary
                              (see config.py and README.md)

    Raises:
        ValueError: Prefix is not implemented
    """
    prefix, identifier = prefixed_identifier.split(':', 1)
    try:
        fulltext_getter = PREFIX_FULLTEXT_GETTER[prefix]
    except KeyError:
        raise ValueError('Prefix {0} unknown.'.format(prefix))

    def save_stream(stream, path):
        """Save a stream to fulltext_dirname/prefix/identifier/path"""
        full_path = os.path.join(fulltext_dirname, prefix, identifier, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'wb') as file:
            for chunk in stream.iter_content(chunk_size=128):
                file.write(chunk)

    return fulltext_getter(identifier, save_stream, config)
