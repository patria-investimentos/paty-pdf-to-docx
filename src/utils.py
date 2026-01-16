from charset_normalizer import from_bytes


def get_encoding(content: bytes) -> str:
    result = from_bytes(content).best()
    if result is None:
        return "utf-8"
    return result.encoding
