from django.test import TestCase, Client
from slackapp.actions.slack_actions import SlackActions
import json

class ActionTest(TestCase):
    """ this test has the following attempts:
    1) get workspace users
    """

    def test_get_workspace_users(self):
        slackActions = SlackActions()
        response = slackActions.get_users()
        self.assertEqual(isinstance(response, list), True)
    
    def test_send_menu(self):
        slackActions = SlackActions()
        meals = [
            'pollo con arroz',
            'pollo con papas'
        ]
        response = slackActions.send_menu_users(meals)
        self.assertEqual(response, True)