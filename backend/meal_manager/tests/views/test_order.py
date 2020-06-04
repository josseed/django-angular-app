from django.test import TestCase, Client
from meal_manager.models import User, Menu, Worker, Order, Meal
from rest_framework import status
from django.urls import reverse
from meal_manager.utils.jwt_token import jwt_payload_handler, jwt_encode_handler
import json

class OrderTest(TestCase):
    """ this test has the following attempts:
    - Get all the orders of a meal.
    """

    client = Client()

    def setUp(self):
        user = User.objects.create_user(
            email = "menu_test@gmail.cl",
            password = "pass",
        )
        user.save()
        payload = jwt_payload_handler(user)
        self.token = jwt_encode_handler(payload)


    def test_get_orders_of_a_meal(self):
        menu = Menu.objects.create(
            name = "menu test 1",
            date = "2020-02-01"
        )
        meal = Meal.objects.create(
            menu_id = menu.id,
            name = "vegetarian mix"
        )
        worker_1 = Worker.objects.create(
            name = "order test",
            slack_id = "sadlgwm2iqw"
        )
        worker_2 = Worker.objects.create(
            name = "order test",
            slack_id = "sadlgwm2iqw"
        )
        Order.objects.create(
            meal_id = meal.id,
            worker_id = worker_2.id,
            date = menu.date
        )
        Order.objects.create(
            meal_id = meal.id,
            worker_id = worker_1.id,
            date = menu.date,
            customization = "without salad"
        )
        response = self.client.get(
            reverse(
                'order_list',
                kwargs = {
                    'menu_id': menu.id,
                    'meal_id': meal.id     
                }
            ),
            content_type='application/json',
            HTTP_AUTHORIZATION = 'JWT ' + self.token
        )
        len_menus = len(json.loads(response.content))
        self.assertEqual(len_menus, 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
