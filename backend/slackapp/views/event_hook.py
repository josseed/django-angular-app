from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import HttpResponse, JsonResponse
from slackapp.bot.meal_bot import MealBot
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
            print(event_msg)
            mealBot = MealBot(event_msg)
            mealBot.run()
            return HttpResponse(status=200)
        
        return HttpResponse(status=200)

