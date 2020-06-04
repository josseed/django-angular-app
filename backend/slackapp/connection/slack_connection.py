from slack import WebClient
from django.conf import settings
from slack.errors import SlackApiError

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
    
    def build_menu_list(self, meals):
        text = ""
        count = 1
        for meal in meals:
            text = text + ":diamond_shape_with_a_dot_inside: *Opción {}*: {} \n\n".format(count, meal)
            count = count + 1
        return text

    def send_menu_to_users(self, meals):
        users = self.get_users()
        for user in users:
            user_name = user['real_name']
            user_id = user['id']
            message = self.build_menu_message(meals, user_name, user_id)
            sended = self.send_menu_by_user(message)
            if not sended:
                return False
        return True

    def build_selected_meal_message(self, meal, user_id):
        return {
            "channel": user_id,
            "icon_emoji": ':shallow_pan_of_food:' ,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "Tu pedido: *{}* a sido registrado, muchas gracias!".format(meal)
                        ),
                    }
                },
            ]
        }
    
    def build_expired_order_message(self, user_id):

        return {
            "channel": user_id,
            "icon_emoji": ':shallow_pan_of_food:' ,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "Los pedidos ya no están disponibles por hoy, lo sentimos."
                        ),
                    }
                },
            ]
        }

    def build_menu_message(self, meals, user_name, user_id):
        
        list_meals = self.build_menu_list(meals)
        return {
            "channel": user_id,
            "icon_emoji": ':shallow_pan_of_food:' ,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "Hola! :wave: {} :blush:\n\n * te dejo el menú de hoy:*".format(user_name)
                        ),
                    }
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": list_meals,
                    },
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "Para responder mandarme tu opción. ej: 1 \n\n Si quieres pedir personalizado puedes agregar un comentario ej: '1 sin tomate'"
                        ),
                    }
                }
            ]
        }
