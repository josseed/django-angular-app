from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from slackapp.actions.slack_actions import SlackActions
import slack
import json

class EventHook(APIView):
    """
    manage the slack events
    """    
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):

        json_dict = json.loads(request.body.decode('utf-8'))
        if json_dict['token'] != settings.VERIFICATION_TOKEN:
            return HttpResponse(status=403)
            
        if 'type' in json_dict:
            if json_dict['type'] == 'url_verification':
                response_dict = {"challenge": json_dict['challenge']}
                return JsonResponse(response_dict, safe=False)
        
        if 'event' in json_dict:
            event_msg = json_dict['event']
            if 'bot_id' in event_msg:
                return HttpResponse(status=204)

        if event_msg['type'] == 'message':
            user = event_msg['user']
            channel = event_msg['channel']
            response_msg = ":wave:, Hello <@%s>" % user
            print(json_dict)
            client = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)
            client.chat_postMessage(channel=channel, text=response_msg)
            slackActions = SlackActions()
            users = slackActions.get_users()
            print(users)
            return HttpResponse(status=200)
        
        return HttpResponse(status=200)

