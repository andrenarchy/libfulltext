"""Stream module"""

def save_to_file(stream, filename='/tmp/bla.pdf'):
    """Save a stream to a file

    Args:
        stream:    stream that should be written to file
        filename:  name of the file to which the stream gets written
    """
    with open(filename, 'wb') as file:
        for chunk in stream.iter_content(chunk_size=128):
            file.write(chunk)
