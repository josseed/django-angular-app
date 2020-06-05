from datetime import datetime
import pytz
from meal_manager.models import Worker, Menu
from slackapp.bot.connection.slack_connection import SlackConnection
from slackapp.bot.messages.message_builder import MessageBuilder
from slackapp.bot.actions.create_order import create_order
from celery import Task
import re


class MealBot(Task):
    """
    this bot manage all the messages coming from slack direct channels.

    expected message_dict = {
        'user': value, - required
        'channel': value, - required
        'text': value - required
    }

    The actions it performs are the following:
    - register a order.
    - validate if is a avaible hour to make any operation.
    - response to the user a custom message related to his events with the following messages:
        - send_unexpected_message
        - send_unexpected_user 
        - send_wrong_selection
        - send_expired_message
        - send_success_selection
        - send_something_happend
    """
    AVAILABLE_START_HOUR = 8
    AVAILABLE_END_HOUR = 23
    TIME_ZONE = pytz.timezone('America/Santiago')
    is_available_time = False
    unexpected_message = False
    slack = SlackConnection()

    def __init__(self, message_dict):
        self.message_dict = message_dict
        self.check_if_avaible_time()

    def check_if_avaible_time(self):
        """
        check if is a available hour for use the bot.
        """
        datetime_CL = datetime.now(self.TIME_ZONE)
        current_hour = int(datetime_CL.strftime("%H"))
        if self.AVAILABLE_START_HOUR < current_hour < self.AVAILABLE_END_HOUR:
            self.is_available_time = True
  
    def get_channel_id(self) -> str:
       return self.message_dict['channel']

    def get_user_id(self) -> str:
        return self.message_dict['user']

    def get_selection_order(self, message_dict) -> int:
        first = int(re.search(r'\d+', message_dict).group())
        return first
    
    def get_customization_message(self, message_dict):
        split_message = message_dict.split()
        if len(split_message) > 1:
            return ' '.join(split_message[1:])
        else: 
            return None

    def check_if_correct_message(self) -> bool:
        """
        this function check if is a correct message_dict

        return True if is correct.
        return False if is not correct.
        """
        try:
            text = self.message_dict['text']
            clean_text = text.strip()
            self.position = self.get_selection_order(clean_text)
            self.customization = self.get_customization_message(clean_text)     
            return True       
        except BaseException:
            return False

    def check_worker(self) -> bool:
        try:
            user_id = self.get_user_id()
            worker = Worker.objects.get(slack_id = user_id)
            self.worker = worker
            return True       
        except BaseException:
            return False

    def check_selection(self) -> bool:
        try:
            today = datetime.now()
            today_str = today.strftime("%Y-%m-%d")
            menu = Menu.objects.get(date = today_str)
            meals = menu.meals.all()
            meal = meals[self.position - 1]
            self.meal = meal
            return True       
        except BaseException:
            return False

    def send_unexpected_message(self):
        try:
            channel_id = self.get_channel_id()
            message_dict = MessageBuilder.build_unexpected_message(channel_id)
            self.slack.send_message(message_dict)
        except BaseException as e:
            print(e)
            print('fails to send unexpected message_dict')
             
    def send_expired_message(self):
        try:
            channel_id = self.get_channel_id()
            message_dict = MessageBuilder.build_expired_time_message(channel_id)
            self.slack.send_message(message_dict)
        except BaseException:
            print('fails to send expired message_dict')
        
    def send_unexpected_user(self):
        try:
            channel_id = self.get_channel_id()
            message_dict = MessageBuilder.build_unexpected_user_message(channel_id)
            self.slack.send_message(message_dict)
        except BaseException:
            print('fails to send unexpected user')
    
    def send_wrong_selection(self):
        try:
            channel_id = self.get_channel_id()
            message_dict = MessageBuilder.build_wrong_selection_message(channel_id)
            self.slack.send_message(message_dict)
        except BaseException:
            print('fails to send wrong selection')
    
    def send_something_happend(self):
        try:
            channel_id = self.get_channel_id()
            message_dict = MessageBuilder.build_something_happend_message(channel_id)
            self.slack.send_message(message_dict)
        except BaseException:
            print('fails to send somthing happend')
    
    def send_success_selection(self):
        try:
            channel_id = self.get_channel_id()
            message_dict = MessageBuilder.build_selected_meal_message(self.meal.name, channel_id)
            self.slack.send_message(message_dict)
        except BaseException as e:
            print(e)
            print('fails to send success selection')
            
    def run(self, *args, **kwargs):
        if not self.is_available_time:
            return self.send_expired_message()

        if not self.check_if_correct_message():
            return self.send_unexpected_message()

        if not self.check_worker():
            return self.send_unexpected_user()

        if not self.check_selection():
            return self.send_wrong_selection()

        order_dict = {
            'worker_id': self.worker.id,
            'meal_position': self.position,
            'customization': self.customization
        }
        if not create_order(order_dict):
            return self.send_something_happend()

        return self.send_success_selection()

            