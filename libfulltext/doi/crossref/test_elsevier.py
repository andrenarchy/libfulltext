# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Unit tests for Elsevier"""

from unittest import TestCase, skip
import requests

from ...config import parse_env
from ...response import assert_sha1
from .elsevier import get_elsevier_fulltext


class GetElsevierFulltextTest(TestCase):
    """Test get_elsevier_fulltext"""

    # The elsevier API key from the environment
    apikey = parse_env()["publishers"]["elsevier"]["apikey"]

    @skip('Elsevier API currently does not return full texts but only page 1 '
          '(re-enable with a working API key)')
    @staticmethod
    def test_sha1():
        """Compare SHA1 and filename"""
        get_elsevier_fulltext(
            '10.1016/j.physletb.2016.07.042',
            assert_sha1('4724fea61643131e32dd4267608f977ffeafb70e', 'fulltext.pdf'),
            apikey=GetElsevierFulltextTest.apikey
        )

    def test_incomplete_pdf(self):
        """An incomplete PDF (restricted to first page) should be detected.
        The DOI is a non-OA article."""
        with self.assertRaises(requests.exceptions.HTTPError) as context:
            get_elsevier_fulltext(
                '10.1016/j.laa.2017.12.020',
                lambda stream, filename: None,
                apikey=GetElsevierFulltextTest.apikey
            )
        self.assertIn('Response limited to first page', str(context.exception))

    def test_non_existent_doi(self):
        """A non-existing DOI should result in an error"""
        with self.assertRaises(requests.exceptions.HTTPError) as context:
            get_elsevier_fulltext(
                '10.1103/non-existent',
                lambda stream, filename: None,
                apikey=GetElsevierFulltextTest.apikey
            )
        self.assertIn('Not Found', str(context.exception))
