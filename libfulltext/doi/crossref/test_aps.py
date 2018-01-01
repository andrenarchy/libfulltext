"""Unit tests for APS"""

from ...test_utils import assert_stream
from .aps import get_aps_fulltext

def test_get_aps_fulltext():
    """Get a fulltext from APS"""
    get_aps_fulltext(
        '10.1103/PhysRevPhysEducRes.13.020141',
        assert_stream('4a1b37cf8dc7699d01b744a1f6da8fbcba8e3b6d', 'fulltext.pdf')
        )
