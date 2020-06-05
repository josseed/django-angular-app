from django.test import TestCase, Client
from slackapp.bot.connection.slack_connection import SlackConnection
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
    
    def test_send_menu_action(self):


        slack = SlackConnection()
        users = slack.get_users()
        for user in users:
            user['url'] = 'http://test_url.cl'
        meals = [
            'chicken with potatoes',
            'vegan mix'
        ]
        response = slack.send_menu_to_users(users, meals)
        self.assertEqual(response, True)