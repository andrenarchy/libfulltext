# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Response functions"""

import hashlib
import requests


def assert_sha1(expected_sha1, expected_path):
    """Returns a function that checks a save_response call via expected SHA1 hash and path

    Args:
        expected_sha1: expected SHA1 hash of the downloaded file
        expected_path: expected basename of the downloaded file

    Returns:
        A function that takes as stream (from a response) and a string
        (basename where the stream should usually be saved). To match the
        interface of save_stream
    """

    def process_response(response, path):
        """Process a response and verify SHA1 hash and path

        Args:
            response: the stream from an API response
            path:     string (unused, normally basename of the output file)

        """
        assert path == expected_path
        sha = hashlib.sha1()
        for chunk in response.iter_content(chunk_size=128):
            sha.update(chunk)
        assert sha.hexdigest() == expected_sha1
    return process_response


def save_to_file(response, filename):
    """Save a stream to a file

    Args:
        stream:    stream that should be written to file
        filename:  name of the file to which the stream gets written
    """
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)


def verify(response, expected_content_type):
    """Verify a response (currently only the status code and content type header)

    Args:
        response:               requests.Response object from an API request
        expected_content_type:  expected Content-Type as string (e.g. 'application/pdf')

    Raises:
        requests.exceptions.InvalidHeader: if content type undeclared or unexpected
    """
    response.raise_for_status()

    if 'Content-Type' not in response.headers or \
            response.headers['Content-Type'] != expected_content_type:
        raise requests.exceptions.InvalidHeader('Content-Type is not ',
                                                expected_content_type, ', ',
                                                'possibly because you do not have access '
                                                'to this document.')
