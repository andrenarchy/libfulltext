# copyright © 2018 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Unit tests for arXiv"""

from unittest import TestCase
import requests
import hashlib

from . import get_arxiv_fulltext


# TODO test if this really works
# TODO merge into response.py
def assert_sha1_checklist(expected_sha1s, expected_paths, checklist):
    """Returns a function that checks a save_response call via expected SHA1 hash and path"""
    for expected_path in expected_paths:
        checklist[expected_path] = False

    def process_response(response, path):
        """Process a response and verify SHA1 hash and path"""
        assert path in expected_paths
        checklist[path] = True
        sha = hashlib.sha1()
        for chunk in response.iter_content(chunk_size=128):
            sha.update(chunk)
        assert sha.hexdigest() == expected_sha1s[expected_paths.index(path)]
    return process_response


class GetArxivFulltextTest(TestCase):
    """Test get_arxiv_fulltext"""

    @staticmethod
    def test_sha1():
        # TODO: I do not understand why this paper cannot be accessed from APS
        """Compare SHA1 and filename"""
        checklist = {}
        get_arxiv_fulltext('1709.01156',
                           assert_sha1_checklist(['44b0d62a091b1dba1a6c92a7ad9ad658bcd59138',
                                                  'fa41a5cea068344bbeafd77ff3cb9d069a2449f8'],
                                                 ['arxiv.pdf',
                                                  'fulltext.pdf'],
                                                 checklist
                                                 ),
                           None
                           )
        assert len(checklist.keys()) == 2
        for target in checklist.keys():
            assert checklist[target]

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
        #self.assertIn('Did not obtain any arXiv article', str(context.exception))
        self.assertIn("Didn't contain a pdf link", str(context.exception))
