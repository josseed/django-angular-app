from django.test import TestCase, Client
from slackapp.connection.slack_connection import SlackConnection
import json

class ActionTest(TestCase):
    """ this test has the following attempts:
    - get workspace users
    - send menu to users in the workspace
    """

    def test_get_workspace_users(self):
        slack = SlackConnection()
        response = slack.get_users()
        self.assertEqual(isinstance(response, list), True)
    
    def test_send_menu(self):
        slack = SlackConnection()
        meals = [
            'pollo con arroz',
            'pollo con papas'
        ]
        response = slack.send_menu_users(meals)
        self.assertEqual(response, True)