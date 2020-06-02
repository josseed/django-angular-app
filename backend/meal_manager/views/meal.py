from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from meal_manager.models import Meal, Menu
from meal_manager.serializers import MealSerializer
from rest_framework import status
from django.core import serializers

class MealList(APIView):
    """
    list all meals of one menu or create a new meal
    """    
    def get_meals(self, menu_id):
        return Meal.objects.filter(menu_id = menu_id)

    def get_menu(self, menu_id):
        try:
            menu = Menu.objects.get(pk = menu_id)
            return menu
        except Menu.DoesNotExist:
            raise Http404
    
    def is_unique_meal(self, menu_id, name_meal):
        try:
            Meal.objects.get(name = name_meal, menu_id = menu_id)
            return False
        except Meal.DoesNotExist:
            return True

    def get(self, request, menu_id, format=None):
        meals = self.get_meals(menu_id) 
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, menu_id, format = None):
        if not request.data.get('name'):
            raise ParseError("name field is required.")
        meal_name = request.data.get('name')
        menu = self.get_menu(menu_id)
        if not self.is_unique_meal(menu.id, meal_name):
            detail = {'detail': 'this menu already has this meal'}
            return Response(detail, status=status.HTTP_409_CONFLICT)

        serializer = MealSerializer(
            data=request.data,
            context = {'menu_id': menu.id}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

