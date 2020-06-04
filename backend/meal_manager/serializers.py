from meal_manager.models import (Worker, Menu, Meal, Order)
from rest_framework import serializers

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'
        read_only_fields = ('menu',)
    
    def create(self, validated_data):
        menu_id = self.context.get('menu_id')
        meal = Meal.objects.create(menu_id = menu_id, **validated_data)
        return meal

class MenuSerializer(serializers.ModelSerializer):
    meals = MealSerializer(read_only=True, many=True)
    class Meta:
        model = Menu
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
