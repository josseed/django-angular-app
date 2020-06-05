from django.test import TestCase, Client
from meal_manager.models import Worker, Menu, Meal, Order
from datetime import date
from meal_manager.tasks.send_menu import SendMenuTask
import json

class SendMenuTest(TestCase):
    """ this test has the following attempts:
    - 
    """

    def setUp(self):
        today = date.today().strftime("%Y-%m-%d")
        menu = Menu.objects.create(
            name = "menu testing create order test",
            date = today
        )
        self.menu_id = menu.id
        Meal.objects.create(
            menu_id = menu.id,
            name = "meal testing"
        )
        Meal.objects.create(
            menu_id = menu.id,
            name = "meal testing two"
        )
        
    def test_send_menu(self):
        data_dict = {
            'menu_id': self.menu_id
        }
        send_menu = SendMenuTask(data_dict)
        send_menu.run()
    