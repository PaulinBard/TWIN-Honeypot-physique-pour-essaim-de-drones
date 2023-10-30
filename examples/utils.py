

def space_hex(h):
    """Prints a string of hex digits with spaces between each byte."""
    return ' '.join(h[i:i+2] for i in range(0, len(h), 2))