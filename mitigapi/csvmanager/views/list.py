import json

from django.http import HttpResponse
from django.views import View

from csvmanager.lib.cvv_loader import CVVLoader


class ListView(View):
    """
    The view of the "list" endpoint.

    GET: Retrieves the cvv files by a topic.

    Example:
        import requests

        requests.get(
            'http://localhost:8000/csv/list/sometopic/'
        )
    Response:
        [
            {"IMAHASH": "https://domaina.tld/cvv/airs.csv"},
            {"IMAHASHTOO": "https://domaina.tld/cvv/afirs.csv"},
            {"IMTHEHASH": "https://domainb.tld/cvv/sairs.csv"}
            . . .
        ]

    TODO: Add error responses codes
    """

    def get(self, request, topic):
        error_message = []
        if topic is None:
            error_message.append('Topic was not found')
        if error_message:  # I want to follow the same pattern
            return HttpResponse(
                json.dumps(
                    {'error': '. '.join(error_message) + '.'}
                ),
                status=400
            )

        try:
            found = CVVLoader.id_and_url_retrieve_many(topic=topic)
        except TypeError as e:
            return HttpResponse(
                json.dumps(
                    {'error': f'Invalid topic received: {topic}'}
                ),
                status=400
            )

        if not found:
            return HttpResponse(
                json.dumps(
                    {'error': f'CVV files not found with topic: {topic}'}
                ),
                status=404
            )

        return HttpResponse(json.dumps(found))
