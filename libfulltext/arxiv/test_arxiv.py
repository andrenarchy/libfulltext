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
        # TODO: expected different API result
        # with self.assertRaises(ValueError) as context:
        with self.assertRaises(requests.exceptions.InvalidHeader) as context:
            get_arxiv_fulltext('physics/0701199',
                               lambda stream, filename: None,
                               None)
        self.assertIn("Content-Type is not application/pdf", str(context.exception))
        # self.assertIn("Didn't contain a pdf link", str(context.exception))

    def test_non_existent_id(self):
        """A non-existing ID should result in an error"""
        with self.assertRaises(PDFLinkExtractionFailure) as context:
            get_arxiv_fulltext('hep-ex/invalid', lambda stream, filename: None, None)
        # TODO: absurdly, this DOES return an entry, just without pdf
        # self.assertIn('Did not obtain any arXiv article', str(context.exception))
        self.assertIn("No PDF link", str(context.exception))
