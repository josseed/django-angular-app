from django.test import TestCase, Client
from django.conf import settings
from meal_manager.models import Worker, Menu, Meal, Order
from datetime import date
from slackapp.bot.actions.create_order import create_order
from slackapp.bot.meal_bot import MealBot
import json

class BotTest(TestCase):
    """
    This class test all the type of responses of the bot
     the following attempts:
    - bot response a expired time message.
    - bot response a unexpected text message.
    - bot response a unexpected user message.
    - bot response a wrong selection message.
    - bot response a something happened message.
    - bot response a success message.
    """
    TEST_USER_SLACK_ID = settings.TEST_USER_SLACK_ID

    def setUp(self):
        today = date.today().strftime("%Y-%m-%d")
        menu = Menu.objects.create(
            name = "menu testing create order test",
            date = today
        )
        meal = Meal.objects.create(
            menu_id = menu.id,
            name = "meal testing"
        )
        worker = Worker.objects.create(
            name = "test worker",
            slack_id = self.TEST_USER_SLACK_ID
        )
        self.worker = worker
        self.meal = meal
        self.position = 1
    
    def set_available_hours(self, bot: MealBot):
        bot.AVAILABLE_START_HOUR = 0
        bot.AVAILABLE_END_HOUR = 24
        return bot
    
    def set_unavailable_hours(self, bot: MealBot):
        bot.AVAILABLE_START_HOUR = 0
        bot.AVAILABLE_END_HOUR = 0
        return bot

    def test_bot_expired_time_message(self):
        message_dict = {
            'channel': self.worker.slack_id,
            'text': f'{self.position}',
            'user': self.worker.slack_id
        }
        bot = MealBot(message_dict)
        bot = self.set_unavailable_hours(bot)
        bot.run()
        bot_runned = bot.get_bot_runned()
        last_type_message = bot.get_last_message_type()
        status_message = bot.get_status_message()
        self.assertTrue(bot_runned)
        self.assertEqual(last_type_message, 0)
        self.assertTrue(status_message)

    def test_bot_unexpected_text_message(self):
        message_dict = {
            'channel': self.worker.slack_id,
            'text': 'bad message',
            'user': self.worker.slack_id
        }
        bot = MealBot(message_dict)
        bot = self.set_available_hours(bot)
        bot.run()
        bot_runned = bot.get_bot_runned()
        last_type_message = bot.get_last_message_type()
        status_message = bot.get_status_message()
        self.assertTrue(bot_runned)
        self.assertEqual(last_type_message, 1)
        self.assertTrue(status_message)

    def test_bot_unexpected_user_message(self):
        message_dict = {
            'channel': self.worker.slack_id,
            'text': f'{self.position}',
            'user': 'a-diferent-id'
        }
        bot = MealBot(message_dict)
        bot = self.set_available_hours(bot)
        bot.run()
        bot_runned = bot.get_bot_runned()
        last_type_message = bot.get_last_message_type()
        status_message = bot.get_status_message()
        self.assertTrue(bot_runned)
        self.assertEqual(last_type_message, 2)
        self.assertTrue(status_message)
    
    def test_bot_wrong_selection_message(self):
        message_dict = {
            'channel': self.worker.slack_id,
            'text': '{}'.format(2),
            'user': self.worker.slack_id
        }
        bot = MealBot(message_dict)
        bot = self.set_available_hours(bot)
        bot.run()
        bot_runned = bot.get_bot_runned()
        last_type_message = bot.get_last_message_type()
        status_message = bot.get_status_message()
        self.assertTrue(bot_runned)
        self.assertEqual(last_type_message, 3)
        self.assertTrue(status_message)
    
    def test_bot_somthing_happened_message(self):
        message_dict = {
            'channel': self.worker.slack_id,
            'text': '{}'.format(self.position),
            'user': self.worker.slack_id
        }
        bot = MealBot(message_dict)
        bot = self.set_available_hours(bot)
        bot.TEST_SOMETHING_HAPPEND = True
        bot.run()
        bot_runned = bot.get_bot_runned()
        last_type_message = bot.get_last_message_type()
        status_message = bot.get_status_message()
        self.assertTrue(bot_runned)
        self.assertEqual(last_type_message, 4)
        self.assertTrue(status_message)
    
    def test_bot_success_order_message(self):
        message_dict = {
            'channel': self.worker.slack_id,
            'text': '{}'.format(self.position),
            'user': self.worker.slack_id
        }
        bot = MealBot(message_dict)
        bot = self.set_available_hours(bot)
        bot.run()
        bot_runned = bot.get_bot_runned()
        last_type_message = bot.get_last_message_type()
        status_message = bot.get_status_message()
        self.assertTrue(bot_runned)
        self.assertEqual(last_type_message, 5)
        self.assertTrue(status_message)


    def test_create_basic_order(self):
        order_dict = {
            'worker_id': self.worker.id,
            'meal_position': self.position
        }
        status = create_order(order_dict)
        self.assertTrue(status)
    
    def test_create_custom_order(self):
        order_dict = {
            'worker_id': self.worker.id,
            'meal_position': self.position,
            'customization': 'can it be with ketchup?'
        }
        status = create_order(order_dict)
        order = Order.objects.get(
            meal_id = self.meal.id,
            worker_id = self.worker.id
        )
        self.assertEqual(order.customization, order_dict['customization'])
        self.assertTrue(status)
