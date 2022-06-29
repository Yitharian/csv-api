from hashlib import sha256
import re
from typing import Optional

RE_SHA256 = r'[a-z0-9]{64}'


def generate_cvv_id(url: str) -> str:
    """
    From the URL generates its sha256 hash.

    :param str url: The cvv file URL.
    :return str: hashed URL
    """
    return sha256(url.encode('utf-8')).hexdigest()


def get_cvv_id(key: str) -> Optional[str]:
    """
    Tries to find the sha256 on the "key", if it was found then returns it,
    else returns None.

    :param str key: Presumed sha256.
    :return str: Found sha256 or None
    """
    if match := re.fullmatch(RE_SHA256, key):
        return match.group(0)
