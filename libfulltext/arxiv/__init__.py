# copyright © 2018 the libfulltext authors (see AUTHORS.md and LICENSE)
"""arXiv handler module"""

import requests
from lxml import etree

from ...response import verify
from ..doi import get_doi_fulltext


def get_arxiv_fulltext(arxiv_id, save_stream, config):
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
        ValueError:           did not obtain exactly one query result or
                              entry did not contain pdf link
        NotImplementedError:  multiple arXiv IDs provided
    """

    if "," in arxiv_id:
        raise NotImplementedError("multiple arXiv IDs not implemented")

    response = requests.get("http://export.arxiv.org/api/query",
                            params={"id_list": arxiv_id})
    tree = etree.fromstring(response.content)

    # './' = restrict search to depth 1 in the tree
    # '{*}' = ignore the namespace (usually "http://www.w3.org/2005/Atom")
    entries = tree.findall("./{*}entry")

    if len(entries) == 1:
        entry = entries[0]
    else:
        if len(entries) > 1:
            raise ValueError("Obtained more than one arXiv article")
        else:
            raise ValueError("Did not obtain any arXiv article")

    pdf_link = None
    for element in entry.findall("./{*}link"):
        if 'title' in element.keys() and element.get("title") == "pdf":
            pdf_link = element.get("href")

    if pdf_link is None:
        raise ValueError("Didn't contain a pdf link")

    response = requests.get(pdf_link,
                            stream=True
                            )

    verify(response, 'application/pdf')

    save_stream(response, 'arxiv.pdf')

    try:
        doi = entry.findall("./{*}doi")[0].text
    except KeyError:
        # no associated DOI
        pass
    else:
        get_doi_fulltext(doi, save_stream, config)
