"""Test utilities"""

import hashlib

def assert_stream(expected_sha1, expected_path):
    """Returns a function that checks a save_stream call via expected SHA1 hash and path"""
    def process_stream(stream, path):
        """Process a stream and verify SHA1 hash and path"""
        assert path == expected_path
        sha = hashlib.sha1()
        for chunk in stream.iter_content(chunk_size=128):
            sha.update(chunk)
        assert sha.hexdigest() == expected_sha1
    return process_stream
