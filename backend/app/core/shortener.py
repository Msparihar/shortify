from nanoid import generate
import string


def create_short_code(size: int = 7) -> str:
    """Generate a short code using nanoid with base62 alphabet"""
    alphabet = string.ascii_letters + string.digits
    return generate(alphabet, size)
