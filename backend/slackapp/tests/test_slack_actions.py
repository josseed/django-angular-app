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
    
    def test_send_menus(self):
        slackActions = SlackActions()
        response = slackActions.send_menu_users()
        self.assertEqual(response, True)