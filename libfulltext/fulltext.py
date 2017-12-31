"""Fulltext retrieval module"""

import os

from .doi import get_doi_fulltext

PREFIX_FULLTEXT_GETTER = {
    'doi': get_doi_fulltext,
}


def get_fulltext(prefixed_identifier, config):
    """Get fulltext for a prefixed ID

    Args:
        prefixed_identifier:  article identifier with prefix
                              (e.g. "doi:10.1016/j.cortex.2015.10.021")
        config:               configuration dictionary
                              (see config.py and README.md)

    Raises:
        ValueError: Prefix is not implemented or not provided by caller
    """
    if ":" not in prefixed_identifier:
        raise ValueError('No prefix provided')

    prefix, identifier = prefixed_identifier.split(':', 1)
    try:
        fulltext_getter = PREFIX_FULLTEXT_GETTER[prefix]
    except KeyError:
        raise ValueError('Prefix {0} unknown.'.format(prefix))

    # fulltext sanitisation:
    fulltext_dirname = os.path.abspath(config["storage"]["fulltext"])

    def save_stream(stream, path):
        """Save a stream to fulltext_dirname/prefix/identifier/path

        There might be several files connected to a DOI, each to be saved under
        a different filename. The actual getter function only provides the
        "path" part of the above full filename, the
        fulltext_dirname/prefix/identifier gets set when save_stream is
        defined.

        Args:
            stream: the data stream that will be stored
            path:   the filename in the pre-configured directory to which the stream
                    should get saved

        Raises:
            ValueError: Malicious parts in the identifier or path can cause
                        collisions with other identifiers or break out of the
                        libfulltext directory.
        """

        destination_path = os.path.join(fulltext_dirname, prefix, identifier, path)

        if not os.path.abspath(destination_path).startswith(fulltext_dirname):
            raise ValueError('Destination path {0} not in {1}'
                             .format(destination_path, fulltext_dirname))

        # .. or . in paths can lead to collisions
        path_elements = destination_path.split('/')
        if '..' in path_elements or '.' in path_elements:
            raise ValueError('Destination path {0} contains ".." or ".".'
                             .format(destination_path))

        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        with open(destination_path, 'wb') as file:
            for chunk in stream.iter_content(chunk_size=128):
                file.write(chunk)

    return fulltext_getter(identifier, save_stream, config)
