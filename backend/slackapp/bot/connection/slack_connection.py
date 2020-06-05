from slack import WebClient
from django.conf import settings
from slack.errors import SlackApiError
from slackapp.bot.messages.message_builder import MessageBuilder
from typing import List

StringList = List[str]

class SlackConnection:
    """ This class has the actions for comunicate with the team in slack.
    you can get the users of the workspace, and send this messages:
    - Get a list of the users of the workspace.
    - Send a meal list as direct message for everyone.
    - Send a order confirmation to a specific user.
    - Send a expired order time message.
    """
    def __init__(self):
        self.client = WebClient(token=settings.BOT_USER_ACCESS_TOKEN)

    def get_users(self) -> list:
        """
        if success return a list value.
        
        if fails return a empty list [].
        """
        tries = 3
        keep = True
        while keep:
            try:
                response = self.client.users_list()
                users = response["members"]
                return users
            except SlackApiError:
                tries = tries - 1
                if tries == 0:
                    keep = False
        return []
    
    def send_message(self, message):
        tries = 3
        keep = True
        while keep:
            try:
                self.client.chat_postMessage(
                    **message
                )
                return True
            except SlackApiError:
                tries = tries - 1
                if tries == 0:
                    keep = False
        return False

    def send_menu_to_users(self, users: list, meals: list):
        """
        this send the menu message to each one of the users
        """
        for user in users:
            user_name = user['real_name']
            user_id = user['id']
            url = user['url']
            message = MessageBuilder.build_menu_message(meals, user_name, user_id, url)
            sended = self.send_message(message)
            if not sended:
                return False
        return True
