import json
from django.contrib import messages


class AjaxMessaging_OLDSTYLE(object):
    """
    Middlware for JSON responses. It adds to each JSON response array with messages from django.contrib.messages framework
    It allows handle messages on a page with javascript
    """

    def process_response(self, request, response):
        if request.is_ajax():
            if response['Content-Type'] in ["application/javascript", "application/json"]:
                try:
                    if isinstance(response.content, bytes):
                        content = json.loads(response.content.decode(response.charset))
                    else:
                        content = json.load(response.content)
                except ValueError:
                    return response

                django_messages = []

                for message in messages.get_messages(request):
                    django_messages.append({
                        "level": message.level,
                        "message": message.message,
                        "extra_tags": message.tags,
                    })

                content['django_messages'] = django_messages

                response.content = json.dumps(content)
        return response


class AjaxMessaging(object):
    """
    Middlware for JSON responses. It adds to each JSON response array with messages from django.contrib.messages framework
    It allows handle messages on a page with javascript
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        if request.is_ajax():
            if response['Content-Type'] in ["application/javascript", "application/json"]:
                try:
                    if isinstance(response.content, bytes):
                        content = json.loads(response.content.decode(response.charset))
                    else:
                        content = json.load(response.content)
                except ValueError:
                    return response

                django_messages = []

                for message in messages.get_messages(request):
                    django_messages.append({
                        "level": message.level,
                        "message": message.message,
                        "extra_tags": message.tags,
                    })

                content['django_messages'] = django_messages

                response.content = json.dumps(content)
        return response