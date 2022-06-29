import json

from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.views import View

from csvmanager.lib.cvv_loader import CVVLoader
from utils import get_cvv_id

url_validator = URLValidator()


class HeadersView(View):
    """
    The view of the "list" endpoint.

    GET: Retrieves the cvv file headers by ID or URL.

    Example:
        import requests

        requests.get(
            'http://localhost:8000/csv/headers/IMAHASH/'
        )
    Response:
        {
            "IMAHASH": {
                "url": "https://domain.tld/csv/Affeurs.csv",
                "headers": ["header", "headertoo", "yepimheader"]
            }
        }

    TODO: Add error responses codes
    """

    def get(self, request, key):
        error_message = []
        if key is None:
            error_message.append('URL or ID was not found.')
        if error_message:  # I want to follow the same pattern
            return HttpResponse(
                json.dumps(
                    {'error': '. '.join(error_message) + '.'}
                ),
                status=400
            )

        # Validate and extract key
        params = {}
        try:
            if url_hash := get_cvv_id(key):
                params['url_hash'] = url_hash
            elif url_validator(key):
                params['url'] = key
        except ValidationError:
            pass

        if not params:
            return HttpResponse(
                json.dumps({'error': f'{key} is not a URL or ID.'}),
                status=400
            )

        try:
            found = CVVLoader.headers_retrieve(query=params)
        except TypeError:
            return HttpResponse(
                json.dumps({'error': f'Invalid URL or ID received: {key}.'}),
                status=400
            )

        if not found:
            return HttpResponse(
                json.dumps(
                    {'error': f'CVV files not found with URL or ID: {key}.'}
                ),
                status=404
            )

        return HttpResponse(json.dumps(found))
