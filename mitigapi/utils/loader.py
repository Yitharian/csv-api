from typing import Optional

import requests


def secret_loader(path: str) -> str:
    """
    Retrieve the file content found in "path".

    Why it is a function? The reason is that actually we use it on the django
    settings to load the database user and password. And the settings file
    must have settings and not defined functions.

    As well, maybe in a future we want to change the way the secrets are
    loaded. These changes must be here, not on the settings file.

    :param str path: The file path.
    :return str: The file content
    """
    with open(path, 'r') as file:
        return file.readline()


def download_content(url: str) -> Optional[bytes]:
    """
    Downloads and returns the URL content. If it found some problem,
    then returns None.

    :param str url: The URL from where download the content.
    :return bytes: The URL content.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return requests.get(url).content
