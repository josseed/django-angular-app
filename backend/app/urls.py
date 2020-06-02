from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('api/v1/meal-resources/', include('meal_manager.urls')),
]
