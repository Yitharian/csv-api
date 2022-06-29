import json

from django.http import HttpResponse
from django.views import View

from csvmanager.lib.cvv_loader import CVVLoader


class AddView(View):
    """
    The view of the "add" endpoint.

    POST: Adds a new CVV fil to the django model.

    Example:
        import requests, json

        data = {
            'url': 'https://someurl/csv/airs.csv',
            'topic': 'test'
        }
        requests.post(
            'http://localhost:8000/csv/add/',
             data=json.dumps(data)
        )
    Response:
        {
            'added': 'IMAHASH'
        }

    TODO: Add error responses codes
    """

    def post(self, request):
        try:
            parameters = json.loads(request.body)
        except json.decoder.JSONDecodeError as e:
            return HttpResponse(
                json.dumps({'error': 'No data found in POST body'}),
                status=400
            )

        error_message = []
        if (topic := parameters.get('topic')) is None:
            error_message.append('Parameter "topic" was not found')
        if (url := parameters.get('url')) is None:
            error_message.append('Parameter "url" was not found')
        if error_message:
            return HttpResponse(
                json.dumps(
                    {'error': '. '.join(error_message) + '.'}
                ),
                status=400
            )

        try:
            url_hash = CVVLoader.add_cvv(
                url=url,
                topic=topic
            )
        except Exception:
            return HttpResponse(
                json.dumps(
                    {'error': 'Unknown problem adding the new cvv file.'}
                ),
                status=500
            )

        if url_hash is None:
            return HttpResponse(
                json.dumps(
                    {'error': 'The cvv file entry can not '
                              'be added due a unknown error'}
                ),
                status=500
            )

        return HttpResponse(
            json.dumps({'added': url_hash})
        )
