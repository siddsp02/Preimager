import random
from hashlib import sha256
from typing import NamedTuple


class Result(NamedTuple):
    message: bytes
    hex_hash: str


def compute_preimage(
    text: str, max_prepend: int = 10, prefix_zeros: int = 2, max_attempts: int = 1000
) -> tuple[bytes, str] | None:
    """Computes and returns the pre-image needed to reproduce a sha256 hash with
    the specified number of prefix or leading zeros.

    The preimage is calculated by generating a random string that gets prepended
    to the original text, and calculating the hex value of the sha256 digest.
    If the number of attempts specified have not been exceeded, the bytes of the
    pre-image, along with its hash (as a hex string) are returned.
    """
    prefix = "0" * prefix_zeros
    max_prepend >>= 1  # Byte sequences are base-256, so each byte is 2 hex digits.
    for _ in range(max_attempts):
        string = random.randbytes(max_prepend).hex()
        message = (text + string).encode()
        message_hash = sha256(message).hexdigest()
        if message_hash.startswith(prefix):
            return Result(message, message_hash)
    return None
