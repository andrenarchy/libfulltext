# copyright © 2018 the libfulltext authors (see AUTHORS.md and LICENSE)
"""libfulltext exceptions"""


class PDFLinkExtractionFailure(Exception):
    """PDF download link could not be found in response"""


class EntryNotFound(Exception):
    """ID was not found on server"""
