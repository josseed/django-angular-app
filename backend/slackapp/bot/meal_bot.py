from datetime import datetime
from meal_manager.models import Worker, Menu
from django.conf import settings
from slackapp.bot.connection.slack_connection import SlackConnection
from slackapp.bot.messages.message_builder import MessageBuilder
from slackapp.bot.actions.create_order import create_order
from celery import Task
import pytz
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
        - send_expired_message
        - send_unexpected_message
        - send_unexpected_user
        - send_wrong_selection   
        - send_something_happend
        - send_success_selection
    """

    AVAILABLE_START_HOUR = settings.AVAILABLE_START_HOUR
    AVAILABLE_END_HOUR = settings.AVAILABLE_END_HOUR
    TIME_ZONE = pytz.timezone(settings.TIME_ZONE_BOT)

    TEST_SOMETHING_HAPPEND = False

    slack = SlackConnection()
    __last_message = 0
    __status_message = False
    __bot_runned = False

    def __init__(self, message_dict: dict):
        self.message_dict = message_dict

    def get_last_message_type(self) -> int:
        """ this bot has the following messages:
        - send_expired_message: 0 
        - send_unexpected_message: 1
        - send_unexpected_user: 2
        - send_wrong_selection: 3
        - send_something_happend: 4
        - send_success_selection: 5
        """
        return self.__last_message
    
    def get_bot_runned(self) -> bool:
        """ return True if the bot was runned at least once.
        """
        return self.__bot_runned

    def get_status_message(self) -> bool:
        """ return True if the last message was sent successfully.
        """
        return self.__status_message

    def __check_if_avaible_time(self):
        """
        check if is a available hour for use the bot.
        """
        datetime_CL = datetime.now(self.TIME_ZONE)
        current_hour = int(datetime_CL.strftime("%H"))
        if self.AVAILABLE_START_HOUR < current_hour < self.AVAILABLE_END_HOUR:
            return True
        return False
  
    def __get_channel_id(self) -> str:
       return self.message_dict['channel']

    def __get_user_id(self) -> str:
        return self.message_dict['user']

    def _get_selection_order(self, message_dict):
        first = int(re.search(r'\d+', message_dict).group())
        return first
    
    def __get_customization_message(self, message_dict):
        split_message = message_dict.split()
        if len(split_message) > 1:
            return ' '.join(split_message[1:])
        else: 
            return None

    def __check_if_correct_message(self) -> bool:
        """
        this function check if is a correct message_dict

        return True if is correct.
        return False if is not correct.
        """
        try:
            text = self.message_dict['text']
            clean_text = text.strip()
            self.position = self._get_selection_order(clean_text)
            self.customization = self.__get_customization_message(clean_text)     
            return True       
        except BaseException:
            return False

    def __check_worker(self) -> bool:
        try:
            user_id = self.__get_user_id()
            worker = Worker.objects.get(slack_id = user_id)
            self.worker = worker
            return True       
        except BaseException:
            return False

    def __check_selection(self) -> bool:
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

    def __send_unexpected_message(self):
        try:
            channel_id = self.__get_channel_id()
            message_dict = MessageBuilder.build_unexpected_message(channel_id)
            self.slack.send_message(message_dict)
            self.__status_message = True
        except BaseException as e:
            print(e)
            print('fails to send unexpected message_dict')
             
    def __send_expired_message(self):
        try:
            channel_id = self.__get_channel_id()
            message_dict = MessageBuilder.build_expired_time_message(channel_id)
            self.slack.send_message(message_dict)
            self.__status_message = True
        except BaseException:
            print('fails to send expired message_dict')
        
    def __send_unexpected_user(self):
        try:
            channel_id = self.__get_channel_id()
            message_dict = MessageBuilder.build_unexpected_user_message(channel_id)
            self.slack.send_message(message_dict)
            self.__status_message = True
        except BaseException:
            print('fails to send unexpected user')
    
    def __send_wrong_selection(self):
        try:
            channel_id = self.__get_channel_id()
            message_dict = MessageBuilder.build_wrong_selection_message(channel_id)
            self.slack.send_message(message_dict)
            self.__status_message = True
        except BaseException:
            print('fails to send wrong selection')
    
    def __send_something_happend(self):
        try:
            channel_id = self.__get_channel_id()
            message_dict = MessageBuilder.build_something_happend_message(channel_id)
            self.slack.send_message(message_dict)
            self.__status_message = True
        except BaseException:
            print('fails to send somthing happend')
    
    def __send_success_selection(self):
        try:
            channel_id = self.__get_channel_id()
            message_dict = MessageBuilder.build_selected_meal_message(self.meal.name, channel_id)
            self.slack.send_message(message_dict)
            self.__status_message = True
        except BaseException as e:
            print(e)
            print('fails to send success selection')
            
    def run(self, *args, **kwargs):
        self.__bot_runned = True

        if not self.__check_if_avaible_time():
            self.__last_message = 0
            return self.__send_expired_message()

        if not self.__check_if_correct_message():
            self.__last_message = 1
            return self.__send_unexpected_message()

        if not self.__check_worker():
            self.__last_message = 2
            return self.__send_unexpected_user()

        if not self.__check_selection():
            self.__last_message = 3
            return self.__send_wrong_selection()

        # this is only for testing the response of something happend.
        if self.TEST_SOMETHING_HAPPEND:
            self.__last_message = 4
            return self.__send_something_happend()

        order_dict = {
            'worker_id': self.worker.id,
            'meal_position': self.position,
            'customization': self.customization
        }
        if not create_order(order_dict):
            self.__last_message = 4
            return self.__send_something_happend()

        self.__last_message = 5
        return self.__send_success_selection()          