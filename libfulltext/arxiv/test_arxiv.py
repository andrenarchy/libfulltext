# copyright © 2018 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Unit tests for arXiv"""

from unittest import TestCase
import requests
import hashlib
from collections import Counter

from . import get_arxiv_fulltext


# TODO test if this really works
# TODO merge into response.py
def assert_sha1_checklist(sha1_dict, checklist):
    """ assert_sha1_checklist

     * Checks the SHA1 hash values of multiple downloaded files.
     * Checks that all downloaded files are expected.
     * Does not check that all expected files are downloaded
       ('checklist' gets filled with downloaded paths)

    Args:
        sha1_dict: A dictionary string->string
                   (keys: downloaded files' basenames, values: their expected SHA1)
        checklist: Empty list that will be filled with downloaded files' basenames

    Returns:
        A function that takes a stream (from a response) and a string
        (basename where the stream should usually be saved). This function
        matches the interface of save_stream.
    """
    assert checklist == []

    def process_response(response, path):
        """Process a response, verify that the paths are expected, check SHA1 hashes

        Args:
            response: the stream from an API response
            path:     string (basename of the output file)

        """
        assert path in sha1_dict.keys()
        checklist.append(path)
        sha = hashlib.sha1()
        for chunk in response.iter_content(chunk_size=128):
            sha.update(chunk)
        assert sha.hexdigest() == sha1_dict[path]
    return process_response


class GetArxivFulltextTest(TestCase):
    """Test get_arxiv_fulltext"""

    @staticmethod
    def test_sha1():
        # TODO: I do not understand why this paper cannot be accessed from APS
        """Compare SHA1 and filename"""
        checklist = []
        expected_sha1s = {'arxiv.pdf': '44b0d62a091b1dba1a6c92a7ad9ad658bcd59138',
                          'fulltext.pdf': 'fa41a5cea068344bbeafd77ff3cb9d069a2449f8',
                          }
        get_arxiv_fulltext('1709.01156',
                           assert_sha1_checklist(expected_sha1s,
                                                 checklist
                                                 ),
                           None
                           )
        # https://stackoverflow.com/a/7829388
        assert Counter(expected_sha1s.keys) == checklist

    def test_missing_pdf(self):
        """Check an arxiv entry without pdf."""
        # TODO: expected different API result
        # with self.assertRaises(ValueError) as context:
        with self.assertRaises(requests.exceptions.InvalidHeader) as context:
            get_arxiv_fulltext('physics/0701199',
                               lambda stream, filename: None,
                               None
                               )
        self.assertIn("Content-Type is not application/pdf", str(context.exception))
        # self.assertIn("Didn't contain a pdf link", str(context.exception))

    def test_non_existent_id(self):
        """A non-existing ID should result in an error"""
        with self.assertRaises(ValueError) as context:
            get_arxiv_fulltext('hep-ex/invalid', lambda stream, filename: None, None)
        # TODO: absurdly, this DOES return an entry, just without pdf
        # self.assertIn('Did not obtain any arXiv article', str(context.exception))
        self.assertIn("Didn't contain a pdf link", str(context.exception))
