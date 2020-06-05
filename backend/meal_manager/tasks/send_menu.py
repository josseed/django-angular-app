from app.celery import app
from celery import Task
from django.conf import settings
from meal_manager.models import Menu, Worker
from slackapp.bot.connection.slack_connection import SlackConnection
import traceback

class SendMenuTask(Task):
    """
    expected data_dict = {
        'menu_id': value, - required
    }
    this task send the menu to all workers of a workspace.
    the steps are the following:
    1) check if the menu exists.
    2) check if the menu contains any meal.
    3) build a list of strings with the meals.
    2) update the users info.
    4) check if the users
    3) send the menu to all the users.
    """
    ignore_result = True

    def __init__(self, data_dict: dict):
        self.check_data_dict(data_dict)
        self.data_dict = data_dict

    def filter_users(self, users: list) -> list:
        """
        this function update the worker model with the new users of the workspace and add the custom url for each user
        clean bots and slack users
        """
        new_users = []
        for user in users:
            if not (user.get('is_bot') or user.get('real_name') == 'Slackbot'):
                worker, _ = Worker.objects.get_or_create(
                    name = user['real_name'],
                    slack_id = user['id'],
                )
                url = settings.URL_VIEW_MENU + str(worker.unique_uuid)
                user['url'] = url
                new_users.append(user)
                if _:
                    print(f'worker {worker.name} added.')
        return new_users
        
    def check_data_dict(self, data_dict):
        if not data_dict.get('menu_id'):
            raise Exception('menu_id is required.')

    def run(self, *args, **kwargs):

        try:
            menu = Menu.objects.get(pk = self.data_dict['menu_id'])
        except Menu.DoesNotExist:
            raise Exception('fails to get menu')

        meals = menu.meals.all()
        if meals.count() == 0:
            raise Exception("menu does not contain any meal")
        
        #build
        meal_list = [meal.name for meal in meals]

        #initialize slack 
        slack = SlackConnection()
        try:
            users = slack.get_users()
            new_users = self.filter_users(users)
        except BaseException:
            raise Exception('fails to update users')
        
        sended = slack.send_menu_to_users(new_users, meal_list)
        if sended:
            print('menu sended correctly.')
            return None
        else:
            raise Exception('fails to send the menu to slack.')
