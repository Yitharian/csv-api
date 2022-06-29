import csv
from typing import List, Optional

from csvmanager.models import CSVFile
from utils import generate_cvv_id, download_content


class CVVLoader:
    """
    Acts like the intermediary between the django data and the view doing
    the needed operations on the models.

    Actually it is not a good solution: we don't want to do HTTP requests on
    the server, CVVLoader maybe must be another service (just the "add_cvv").
    Also, maybe we only need to save in the django model the URI from another
    database (like s3) as a "content" and do these requests in another service.
    """

    SEPARATOR = ','

    @classmethod
    def add_cvv(cls, url: str, topic: str) -> Optional[str]:
        """
        Add a new "cvv file" to the django model. Note that we do here a HTTP
        request, inside of "download_content".

        :param str url: The URL from where download the cvv file content.
        :param str topic: The topic associated to this cvv file.
        :return str: The ID (it's a hash) of the new entry.
        """
        if (data := download_content(url)) is None:
            return

        try:
            headers = cls._extract_headers(data)
        except Exception as e:
            return

        url_hash = generate_cvv_id(url)

        csv_file = CSVFile(
            url_hash=url_hash,
            url=url,
            topic=topic,
            headers=cls._serialize_headers(headers),
            raw_content=data
        )

        csv_file.save()

        return url_hash

    @classmethod
    def id_and_url_retrieve_many(cls, topic: str) -> List[dict]:
        """
        Finds and returns the cvv files associated to the topic "topic".

        TODO: REALLY IMPORTANT, the param topic must be validated and sanitized
              It belongs to a unknown environment, so it is a potential
              injection attack.

        :param str topic: The topic to do the search on the database.
        :return list: The found cvv files as a list of dictionaries with
        the url_hash as a key and the url in plaintext as a value.
        """
        return [
            {cvv_file.url_hash: cvv_file.url}
            for cvv_file in CSVFile.objects.filter(topic=topic)
        ]

    @classmethod
    def headers_retrieve(cls, query: dict) -> Optional[dict]:
        """
        Retrieves the cvv files headers using the "query" to it. These query
        can be, for example, "{'url': 'hxxp://toto.tld/varinto'}".

        :param dict query: the query as a dictionary where the key is a
        model attribute and the value is its content.
        :return dict: If it found the cvv file then returns it only with the
        url, the url_hash and the headers.
        """
        if cvv_file := CSVFile.objects.filter(**query):
            cvv_file = cvv_file[0]

            headers = cvv_file.headers
            if not isinstance(headers, bytes):
                headers = cvv_file.headers.tobytes()
            headers = headers.decode().split(cls.SEPARATOR)

            return {
                cvv_file.url_hash: {
                    'url': cvv_file.url,
                    'headers': headers
                }}

    @classmethod
    def _extract_headers(cls, data: bytes) -> List[str]:
        """
        Extract the headers from a cvv binary file.

        :param bytes data: cvv binary file
        :return list: The headers as a list.
        """
        tt = data.decode().split('\n')
        data = csv.reader(tt, delimiter=',')
        return data.__next__()

    @classmethod
    def _serialize_headers(cls, headers: List[str]):
        """
        It transforms the headers list to a comma-separated string and
        transforms it to bytes.

        TODO: This function must be some-how in the django model, as well
              with its reverse too.

        :param list headers: The list of headers.
        :return bytes: Encoded comma-separated headers as a bytes
        """
        return (f'{cls.SEPARATOR}'.join(headers)).encode()
