from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from toggl_slack_api.utils import get_toggl_post_slack


@csrf_exempt
def index(request):
    if request.method == 'POST':
        if request.POST['token'] == settings.SLACK_OUTGOING_HOOK_TOKEN:
            response = JsonResponse({
                "text": "African or European?"
            })
            get_toggl_post_slack()
            return response
    return HttpResponse('Unauthorized', status=401)
