from django.db import models


class CSVFile(models.Model):
    """
    Represents a CVV file as a django model.

    :param str url_hash: The ID of the file, it is the hash of the URL field.
    :param str url: The URL from where the cvv content was downloaded.
    :param str headers: The cvv file headers.
    :param str topic: Topic associated to the cvv file.
    :param str raw_content: The cvv file content as a binary
    """
    url_hash = models.CharField(max_length=200, primary_key=True)
    url = models.CharField(max_length=2048)  # Current max URL length
    headers = models.BinaryField()  # TODO: Think about it
    topic = models.CharField(max_length=200)
    raw_content = models.BinaryField()

    # TODO: indexes
