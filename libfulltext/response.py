# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Response functions"""

import hashlib
import requests

def assert_sha1(expected_sha1, expected_path):
    """Returns a function that checks a save_response call via expected SHA1 hash and path"""
    def process_response(response, path):
        """Process a response and verify SHA1 hash and path"""
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
    """Verify a response (currently only the status code and content type header)"""
    response.raise_for_status()

    if 'Content-Type' not in response.headers or \
            response.headers['Content-Type'] != expected_content_type:
        raise requests.exceptions.InvalidHeader('Content-Type is not application/pdf, '
                                                'possibly because you do not have access to '
                                                'this document.')
