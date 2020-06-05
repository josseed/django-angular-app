class MessageBuilder:

    @staticmethod 
    def build_menu_list(meals) -> str:
        text = ""
        count = 1
        for meal in meals:
            text = text + ":diamond_shape_with_a_dot_inside: *Opción {}*: {} \n\n".format(count, meal)
            count = count + 1
        return text
    
    @staticmethod
    def build_selected_meal_message(meal, slack_id) -> dict:
        return {
            "channel": slack_id,
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
    
    @staticmethod
    def build_something_happend_message(slack_id) -> dict:
        return {
            "channel": slack_id,
            "icon_emoji": ':shallow_pan_of_food:' ,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "Algo extraño me ha pasado, por favor contacta un medico de bot!"
                        ),
                    }
                },
            ]
        }

    @staticmethod
    def build_expired_time_message(slack_id) -> dict:

        return {
            "channel": slack_id,
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

    @staticmethod
    def build_unexpected_message(slack_id) -> dict:

        return {
            "channel": slack_id,
            "icon_emoji": ':shallow_pan_of_food:' ,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "Tu mensaje no pudo ser procesado, por favor prueba enviando tu opción ej:'1' o con un comentario ej: '1 sin tomate'."
                        ),
                    }
                },
            ]
        }

    @staticmethod
    def build_unexpected_user_message(slack_id) -> dict:

        return {
            "channel": slack_id,
            "icon_emoji": ':shallow_pan_of_food:' ,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "Lo sentimos, tu usuario no fue reconocido por nuestro sistema, favor contactar a mealapp.cornershop.cl"
                        ),
                    }
                },
            ]
        }

    @staticmethod
    def build_wrong_selection_message(slack_id) -> dict:

        return {
            "channel": slack_id,
            "icon_emoji": ':shallow_pan_of_food:' ,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "Lo sentimos, tu opción ingresada no es valida, favor intenta con las opciones disponibles."
                        ),
                    }
                },
            ]
        }

    @staticmethod
    def build_menu_message(meals, user_name, slack_id, url) -> dict:
        list_meals = MessageBuilder.build_menu_list(meals)
        return {
            "channel": slack_id,
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
                            "Para responder por favor mandame tu opción antes de las 11 AM. ej: 1 \n\n Si quieres pedir personalizado puedes agregar un comentario ej: '1 sin tomate'"
                        ),
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "para ver el menu de hoy puedes entrar a este enlace: {}".format(url)
                        ),
                    }
                }
            ]
        }
