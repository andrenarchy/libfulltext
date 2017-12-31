"""Unit tests for Springer"""

from ...test_utils import assert_stream
from .springer import get_springer_fulltext

def test_get_springer_fulltext():
    """Get a fulltext from Springer"""
    get_springer_fulltext(
        '10.1140/epjc/s10052-016-4338-8',
        assert_stream('4d188155b7d395356d6f62794f41cc6d083296b0', 'fulltext.pdf')
        )
