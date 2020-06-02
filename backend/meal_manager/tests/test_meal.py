from django.test import TestCase, Client
from meal_manager.models import User, Menu, Meal
from rest_framework import status
from django.urls import reverse
from meal_manager.utils.jwt_token import jwt_payload_handler, jwt_encode_handler
import json

class MealTest(TestCase):
    """ this test has the following attempts:
    1) create a valid meal and expect a 201 status code.
    2) trying to create a invalid meal and expect a 400 status code.
    3) trying to create a meal has unauthorized user and expect a 401 status code.
    4) trying to get the meal list has unauthorized user and expect a 401 status code.
    5) trying to create two meals with the same name for the same menu and expect a 409 status code.
    6) trying to create a meal for an unexist menu and expect a 404 code
    7) create two meals and get the list of meals expecting a 200 status code and length 2.
    """

    client = Client()

    def create_data(self):

        user = User.objects.create_user(
            email = "menu_test@gmail.cl",
            password = "pass",
        )
        user.is_active = True
        user.save()
        payload = jwt_payload_handler(user)
        self.token = jwt_encode_handler(payload)

        menu = Menu.objects.create(
            name = "menu_test_meal",
            date = "2020-01-01"
        )
        self.menu_id = menu.id


    def setUp(self):
        self.create_data()
        self.valid_payload = {
            "name": "chicken with potatoes",
        }
        self.invalid_payload = {
            "any-key": "chicken with potatoes"
        }

    def test_create_valid_meal(self):
        response = self.client.post(
            reverse(
                'meal_list',
                kwargs = {'menu_id': self.menu_id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION = 'JWT ' + self.token
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_meal(self):
        response = self.client.post(
            reverse(
                'meal_list',
                kwargs = {'menu_id': self.menu_id}
            ),
            data=json.dumps(self.invalid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION = 'JWT ' + self.token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_meal_unauthorized(self):
        response = self.client.post(
            reverse(
                'meal_list',
                kwargs = {'menu_id': self.menu_id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_meal_unauthorized(self):
        response = self.client.get(
            reverse(
                'meal_list',
                kwargs = {'menu_id': self.menu_id}
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_meals_of_one_menu(self):
        Meal.objects.create(
            menu_id = self.menu_id,
            name = "vegan food"
        )
        Meal.objects.create(
            menu_id = self.menu_id,
            name = "chicken food"
        )
        response = self.client.get(
            reverse(
                'meal_list',
                kwargs = {'menu_id': self.menu_id}
            ),
            content_type='application/json',
            HTTP_AUTHORIZATION = 'JWT ' + self.token
        )
        len_menus = len(json.loads(response.content))
        self.assertEqual(len_menus, 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_meal_in_unexist_menu(self):
        response = self.client.post(
            reverse(
                'meal_list',
                kwargs = {'menu_id': 125126}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION = 'JWT ' + self.token
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_two_equal_meals_for_the_same_menu(self):
        self.client.post(
            reverse(
                'meal_list',
                kwargs = {'menu_id': self.menu_id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION = 'JWT ' + self.token
        )
        response = self.client.post(
            reverse(
                'meal_list',
                kwargs = {'menu_id': self.menu_id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION = 'JWT ' + self.token
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
