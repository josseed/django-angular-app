from django.test import TestCase, Client
from meal_manager.models import User, Menu, Worker
from rest_framework import status
from datetime import date
from django.urls import reverse
from meal_manager.utils.jwt_token import jwt_payload_handler, jwt_encode_handler
import json

class MenuTest(TestCase):
    """ this test has the following attempts:
    - Create a valid menu and expect a 201 status code.
    - Trying to create a invalid menu and expet a 400 status code.
    - Trying to create a munu has unauthorized user and expect a 401 status code.
    - Trying to get the menu list has unauthorized user and expect a 401 status code.
    - Trying to create two menus for the same day and expect a 409 status code.
    - Create two menus and get the list of menus expecting a 200 status code and length 2.
    """

    client = Client()

    def create_data(self):
        user = User.objects.create_user(
            email = "menu_test@gmail.cl",
            password = "pass",
        )
        user.save()
        payload = jwt_payload_handler(user)
        self.token = jwt_encode_handler(payload)

    def setUp(self):
        self.create_data()
        self.valid_payload = {
            "name": "menu 1",
            "date": "2020-06-02"
        }
        self.invalid_payload = {
            "name": "menu 1"
        }

    def test_create_valid_menu(self):
        response = self.client.post(
            reverse('menu_list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION = 'JWT ' + self.token
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_menu(self):
        response = self.client.post(
            reverse('menu_list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION = 'JWT ' + self.token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_menu_unauthorized(self):
        response = self.client.post(
            reverse('menu_list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_menus_unauthorized(self):
        response = self.client.get(
            reverse('menu_list'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_menus(self):
        Menu.objects.create(
            name = "menu test 1",
            date = "2020-02-01"
        )
        Menu.objects.create(
            name = "menu test 2",
            date = "2020-02-02"
        )
        response = self.client.get(
            reverse('menu_list'),
            content_type='application/json',
            HTTP_AUTHORIZATION = 'JWT ' + self.token
        )
        len_menus = len(json.loads(response.content))
        self.assertEqual(len_menus, 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_two_menus_for_same_day(self):
        self.client.post(
            reverse('menu_list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION = 'JWT ' + self.token
        )
        response = self.client.post(
            reverse('menu_list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION = 'JWT ' + self.token
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    
    def test_get_current_menu_by_uuid(self):
        today = date.today().strftime("%Y-%m-%d")
        Menu.objects.create(
            name = "menu test uuid",
            date = today
        )
        worker = Worker.objects.create(
            name = "worker test uuid",
            slack_id = 'any-slack-id'
        )
        response = self.client.get(
            reverse(
                'current_menu_by_uuid',
                kwargs = {
                    'uuid': worker.unique_uuid
                }
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_current_menu(self):
        today = date.today().strftime("%Y-%m-%d")
        Menu.objects.create(
            name = "menu test uuid",
            date = today
        )
        worker = Worker.objects.create(
            name = "worker test uuid",
            slack_id = 'any-slack-id'
        )
        response = self.client.get(
            reverse('current_menu'),
            content_type='application/json',
            HTTP_AUTHORIZATION = 'JWT ' + self.token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
