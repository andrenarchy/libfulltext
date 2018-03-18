# copyright © 2018 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Unit tests for arXiv"""

from unittest import TestCase
import requests

from . import get_arxiv_fulltext
from ..response import assert_sha1
from ..exceptions import PDFLinkExtractionFailure


class GetArxivFulltextTest(TestCase):
    """Test get_arxiv_fulltext"""

    @staticmethod
    def test_sha1():
        """Compare SHA1 and filename"""
        get_arxiv_fulltext(
            '1709.01156',
            assert_sha1('44b0d62a091b1dba1a6c92a7ad9ad658bcd59138', 'arxiv.pdf'),
            None)

    def test_missing_pdf(self):
        """Check an arxiv entry without pdf."""
        # One would expect a libfulltext.exceptions.PDFLinkExtractionFailure
        # exception here, but the API actually returns a pdf link, which just
        # doesn't provide a downloadable pdf. (And a human readable error
        # message)
        with self.assertRaises(requests.exceptions.InvalidHeader) as context:
            get_arxiv_fulltext('physics/0701199',
                               lambda stream, filename: None,
                               None)
        self.assertIn("Content-Type is not application/pdf", str(context.exception))
        # self.assertIn("Didn't contain a pdf link", str(context.exception))

    def test_non_existent_id(self):
        """A non-existing ID should result in an error"""
        # One would expect a libfulltext.exceptions.EntryNotFound exception
        # here, but the API actually returns a pdf link, which just doesn't
        # provide a downloadable pdf. (And a human readable error message)
        with self.assertRaises(PDFLinkExtractionFailure) as context:
            get_arxiv_fulltext('hep-ex/invalid', lambda stream, filename: None, None)
        self.assertIn("No PDF link", str(context.exception))
