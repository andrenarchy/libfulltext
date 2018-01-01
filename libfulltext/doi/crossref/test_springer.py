"""Unit tests for Springer"""

from unittest import TestCase

from ...test.utils import assert_stream
from .springer import get_springer_fulltext

class GetSpringerFulltextTest(TestCase):
    """Test get_springer_fulltext"""

    @staticmethod
    def test_sha1():
        """Compare SHA1 and filename"""
        get_springer_fulltext(
            '10.1140/epjc/s10052-016-4338-8',
            assert_stream('4d188155b7d395356d6f62794f41cc6d083296b0', 'fulltext.pdf')
            )

    def test_non_existent_doi(self):
        """A non-existing DOI should result in an error"""
        with self.assertRaises(Exception) as context:
            get_springer_fulltext('10.1140/epjc/non-existent', lambda stream, filename: None)
        self.assertIn('Not Found', str(context.exception))
