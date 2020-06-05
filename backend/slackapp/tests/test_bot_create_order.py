from django.test import TestCase, Client
from meal_manager.models import Worker, Menu, Meal, Order
from datetime import date
from slackapp.bot.actions.create_order import create_order
import json

class CreateOrderTest(TestCase):
    """ this test has the following attempts:
    - Create a basic order and expect a true value.
    - Create a custom order and expect a true value.
    """

    def setUp(self):
        today = date.today().strftime("%Y-%m-%d")
        menu = Menu.objects.create(
            name = "menu testing create order test",
            date = today
        )
        meal = Meal.objects.create(
            menu_id = menu.id,
            name = "meal testing"
        )
        self.meal_id = meal
        self.position = 1

    def test_create_basic_order(self):
        worker = Worker.objects.create(
            name = "test worker",
            slack_id = "2150fw"
        )
        order_dict = {
            'worker_id': worker.id,
            'meal_position': self.position
        }
        status = create_order(order_dict)
        self.assertEqual(status, True)
    
    def test_create_custom_order(self):
        worker = Worker.objects.create(
            name = "test worker 2",
            slack_id = "2150fwasd"
        )
        order_dict = {
            'worker_id': worker.id,
            'meal_position': self.position,
            'customization': 'can it be with ketchup?'
        }
        status = create_order(order_dict)
        order = Order.objects.get(
            meal_id = self.meal_id,
            worker_id = worker.id
        )
        self.assertEqual(order.customization, order_dict['customization'])
        self.assertEqual(status, True)
