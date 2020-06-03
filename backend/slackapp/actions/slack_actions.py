from slack import WebClient
from django.conf import settings
from slack.errors import SlackApiError

class SlackActions:

    def __init__(self):
        self.client = WebClient(token=settings.BOT_USER_ACCESS_TOKEN)

    def get_users(self):
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
    
    def send_menu_by_user(self, message):
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

    def build_menu_message(self, menu, user_name, user_id):

        return {
            "channel": user_id,
            "icon_emoji": ':shallow_pan_of_food:' ,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "Hola! :wave: {} :blush:\n\n *les dejo el menú de hoy:*".format(user_name)
                        ),
                    }
                }
            ]
        }


    def send_menu_users(self):
        users = self.get_users()
        for user in users:
            user_name = user['real_name']
            user_id = user['id']
            message = self.build_menu_message(None, user_name, user_id)
            sended = self.send_menu_by_user(message)
            if not sended:
                return False
        return True
