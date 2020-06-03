from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from meal_manager.models import Meal, Menu, Order
from meal_manager.serializers import OrderSerializer
from rest_framework import status
from django.core import serializers

class OrderMenuList(APIView):
    """
    List all orders of a menu
    """    
    def get_orders(self, menu_id):
        return Order.objects.filter(meal__menu_id = menu_id)

    def get_menu(self, menu_id):
        try:
            menu = Menu.objects.get(pk = menu_id)
            return menu
        except Menu.DoesNotExist:
            raise Http404

    def get(self, request, menu_id, format=None):
        menu = self.get_menu(menu_id)
        meals = self.get_orders(menu.id) 
        serializer = OrderSerializer(meals, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class OrderMealList(APIView):
    """
    List all orders of a meal or create a new order.
    """
    def get_orders(self, meal_id):
        return Order.objects.filter(order_id = meal_id)
    
    def get_meal(self, menu_id, meal_id):
        try:
            meal = Meal.objects.get(pk = meal_id, menu_id = menu_id)
            return meal
        except Meal.DoesNotExist:
            raise Http404
    
    def get(self, request, menu_id, meal_id, format=None):
        meal = self.get_meal(menu_id, meal_id)
        orders = self.get_orders(meal.id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
