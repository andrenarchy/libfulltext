# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Unit tests for APS"""

from unittest import TestCase

from ...response import assert_sha1
from .aps import get_aps_fulltext

class GetApsFulltextTest(TestCase):
    """Test get_aps_fulltext"""

    @staticmethod
    def test_sha1():
        """Compare SHA1 and filename"""
        get_aps_fulltext(
            '10.1103/PhysRevPhysEducRes.13.020141',
            assert_sha1('4a1b37cf8dc7699d01b744a1f6da8fbcba8e3b6d', 'fulltext.pdf')
            )

    def test_no_access(self):
        """No access should be detected."""
        with self.assertRaises(Exception) as context:
            get_aps_fulltext(
                '10.1103/PhysRevA.96.063419',
                lambda stream, filename: None,
                )
        self.assertIn('Unauthorized', str(context.exception))

    def test_non_existent_doi(self):
        """A non-existing DOI should result in an error"""
        with self.assertRaises(Exception) as context:
            get_aps_fulltext('10.1103/non-existent', lambda stream, filename: None)
        self.assertIn('Not Found', str(context.exception))
