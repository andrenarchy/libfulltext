# copyright © 2018 the libfulltext authors (see AUTHORS.md and LICENSE)
"""arXiv handler module"""

import re
import requests
from lxml import etree

from ..response import verify
from ..exceptions import PDFLinkExtractionFailure
from ..exceptions import EntryNotFound


def get_arxiv_fulltext(arxiv_id, save_stream, config):
    # pylint: disable=unused-argument
    """Get the fulltext for an arXiv ID

    At the moment meant to handle one arXiv ID at a time, though the arxiv
    API can handle multiple IDs (comma separated).

    Args:
        arxiv_id:    arxiv ID string (with prefix)
        save_stream: function that saves a stream (arguments: stream, path)
        config:      configuration dictionary (see config.py)

    Returns:
        What the actual getter returns (usually None)

    Raises:
        ValueError:           function was not called with exactly one ID
        NotImplementedError:  multiple arXiv IDs provided
        requests.exceptions.InvalidHeader:
                              the Content-Type of the pdf download is not that of a pdf
        libfulltext.exceptions.PDFLinkExtractionFailure:
                              the arXiv response does not except exactly one pdf link
        libfulltext.exceptions.EntryNotFound:
                              the arXiv response did not contain an entry
    """

    if "," in arxiv_id:
        raise NotImplementedError("multiple arXiv IDs not implemented")

    response = requests.get("http://export.arxiv.org/api/query",
                            params={"id_list": arxiv_id})
    tree = etree.fromstring(response.content)

    # './' = restrict search to depth 1 in the tree
    # '{*}' = ignore the namespace (usually "http://www.w3.org/2005/Atom")
    entries = tree.findall("./{*}entry")

    if len(entries) > 1:
        raise ValueError("Obtained more than one arXiv article")
    elif not entries:
        raise EntryNotFound("arXiv entry for ID {} not found.".format(arxiv_id))

    entry = entries[0]
    # the document's DOI is at `doi = entry.findall("./{*}doi")[0].text`

    try:
        canonical_id = entry.findall("./{*}id")[0].text
    except KeyError:
        print("The canonical arXiv ID for {} wasn't found in the server"
              " response.".format(arxiv_id))

    canonical_id = re.sub(".*/", "", entry.findall("./{*}id")[0].text)
    if canonical_id != arxiv_id:
        print("The provided ID {} doesn't seem to be canonical, it resolves to"
              " {}.".format(arxiv_id, canonical_id))

    pdf_links = []
    for element in entry.findall("./{*}link"):
        if 'title' in element.keys() and element.get("title") == "pdf":
            pdf_links.append(element.get("href"))

    if not pdf_links:
        raise PDFLinkExtractionFailure("No PDF link in {} response found."
                                       .format(arxiv_id))
    elif len(pdf_links) > 1:
        raise PDFLinkExtractionFailure("Multiple PDF links in {} response found."
                                       .format(arxiv_id))

    response = requests.get(pdf_links[0],
                            stream=True)

    verify(response, 'application/pdf')

    save_stream(response, 'arxiv.pdf')
