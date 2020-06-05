from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from meal_manager.models import Menu, Worker
from rest_framework.permissions import AllowAny
from meal_manager.serializers import MenuSerializer
from rest_framework import status
from django.core import serializers
from meal_manager.tasks.send_menu import SendMenuTask
from datetime import date

class MenuList(APIView):
    """
    list all menus or create a new menu
    """    
    def get_menus(self):
        return Menu.objects.all()

    def is_unique_menu_day(self, date):
        try:
            Menu.objects.get(date = date)
            return False
        except Menu.DoesNotExist:
            return True
    
    def get(self, request, format=None):
        menus = self.get_menus() 
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format = None):
        if not request.data.get('date'):
            raise ParseError("date field is required.")
        menu_date = request.data.get('date')
        if not self.is_unique_menu_day(menu_date):
            detail = {'detail': 'this day already has a menu.'}
            return Response(detail, status=status.HTTP_409_CONFLICT)
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MenuDetail(APIView):
    """
    Get a specific menu
    """

    def get_menu(self, menu_id):
        try:
            menu = Menu.objects.get(pk = menu_id)
            return menu
        except Menu.DoesNotExist:
            raise Http404
    
    def get(self, request, menu_id, format=None):
        menu = self.get_menu(menu_id)
        serializer = MenuSerializer(menu)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SendMenu(APIView):
    """
    Send the menu to workers
    """
    def get_menu(self, menu_id):
        try:
            menu = Menu.objects.get(pk = menu_id)
            return menu
        except Menu.DoesNotExist:
            raise Http404
    
    def post(self, request, menu_id, format=None):
        menu = self.get_menu(menu_id)
        meals = menu.meals.all()
        if meals.count() == 0:
            json_dict = {'detail': "this menu don't have any meal, please create at least one."}
            return Response(json_dict, status=status.HTTP_409_CONFLICT)
        celery_dict = {
            'menu_id': menu.id
        }
        send_menu = SendMenuTask(celery_dict)   
        send_menu.run()
        json_dict = {'detail': 'menu sended.'}
        return Response(json_dict, status=status.HTTP_200_OK)

class CurrentMenuByUUID(APIView):
    """
    Get the menu for the current day if is a valid uuid for any worker.
    """
    permission_classes = (AllowAny,)

    def check_worker_by_uuid(self, uuid):
        try:
            Worker.objects.get(unique_uuid = uuid)
        except Worker.DoesNotExist:
            raise Http404
    
    def get_current_menu(self):
        try:
            today = date.today().strftime("%Y-%m-%d")
            menu = Menu.objects.get(date = today)
            return menu
        except Menu.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        if request.user.is_anonymous:
            self.check_worker_by_uuid(uuid)
        
        menu = self.get_current_menu()
        serializer = MenuSerializer(menu)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

