from django.db import models
from django.contrib.auth.models import AbstractUser
from meal_manager.utils.user_manager import CustomUserManager
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()
    def __str__(self):
        return self.email

class Worker(models.Model):
    name = models.CharField(max_length=100)
    slack_id = models.TextField()
    active = models.BooleanField(default=True)
    date_update = models.DateTimeField(auto_now=True)
    date_creation = models.DateTimeField(auto_now_add=True)

class Menu(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(unique=True)
    date_update = models.DateTimeField(auto_now=True)
    date_creation = models.DateTimeField(auto_now_add=True)

class Meal(models.Model):
    name = models.CharField(max_length=100)
    menu = models.ForeignKey(Menu, related_name='meals', on_delete=models.CASCADE)
    date_update = models.DateTimeField(auto_now=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('menu', 'name')

class Order(models.Model):
    meal = models.ForeignKey(Meal, related_name='orders', on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, related_name='orders', on_delete=models.CASCADE)
    customization = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    date_update = models.DateTimeField(auto_now=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('worker', 'date')

