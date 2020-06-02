from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from meal_manager.utils.create_data import create_nora_user
from meal_manager.views import (menu, meal)

create_nora_user()

urlpatterns = [
    path(
        'auth/login',
        obtain_jwt_token,
        name = 'obtain_jwt_token'
    ),
    path('menus',
        menu.MenuList.as_view(),
        name = 'menu_list'
    ),
    path('menus/<int:menu_id>/meals',
        meal.MealList.as_view(),
        name = 'meal_list'
    )
]