"""Fulltext retrieval module"""

import os

from .doi import get_doi_fulltext

PREFIX_FULLTEXT_GETTER = {
    'doi': get_doi_fulltext,
}

def get_fulltext(config, prefixed_identifier, fulltext_dirname):
    """Get fulltext for a prefixed ID"""
    prefix, identifier = prefixed_identifier.split(':', 1)
    try:
        fulltext_getter = PREFIX_FULLTEXT_GETTER[prefix]
    except KeyError:
        raise ValueError('Prefix {0} unknown.'.format(prefix))

    def save_stream(stream, path):
        """Save a stream to fulltext_dirname/prefix/identifier/path"""
        full_path = '{0}/{1}/{2}/{3}'.format(fulltext_dirname, prefix, identifier, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'wb') as file:
            for chunk in stream.iter_content(chunk_size=128):
                file.write(chunk)

    return fulltext_getter(config, identifier, save_stream)
