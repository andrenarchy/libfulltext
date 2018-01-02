"""Utils for libfulltext"""

import requests

def verify_response(response, expected_content_type):
    """Verify a response (currently only the status code and content type header)"""
    response.raise_for_status()

    if 'Content-Type' not in response.headers or \
            response.headers['Content-Type'] != expected_content_type:
        raise requests.exceptions.InvalidHeader('Content-Type is not application/pdf, '
                                                'possibly because you do not have access to '
                                                'this document.')
