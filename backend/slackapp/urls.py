from django.urls import include, path
from slackapp.views import event_hook

urlpatterns = [
    path('event/hook/', event_hook.EventHook.as_view(), name='event_hook'),
]