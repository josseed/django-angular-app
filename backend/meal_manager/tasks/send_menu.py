from app.celery import app
from django.conf import settings
from meal_manager.models import Menu, Worker
from slackapp.connection.slack_connection import SlackConnection
import traceback


def update_users(users):

    for user in users:
        worker, _ = Worker.objects.get_or_create(
            name = user['real_name'],
            slack_id = user['id']
        )
        if _:
            print(f'worker {worker.name} added.')


@app.task
def send_menu(data):
    """
    this task send the menu to all workers of a workspace.
    the steps are the following:
    1) check if the menu exists.
    2) check if the menu contains any meal.
    3) build a list of strings with the meals.
    2) update the users info.
    4) check if the users
    3) send the menu to all the users.
    """
    #checking
    if not data.get('menu_id'):
        raise Exception('menu_id is required.')
    try:
        menu = Menu.objects.get(pk = data['menu_id'])
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
        update_users(users)
    except:
        raise Exception('fails to update users')
    
    sended = slack.send_menu_to_users(meal_list)
    if sended:
        print('menu sended correctly.')
        return None
    else:
        raise Exception('fails to send the menu to slack.')

