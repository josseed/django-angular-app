from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from meal_manager.utils.create_data import create_nora_user
from meal_manager.views import (menu, meal, order)

create_nora_user()

urlpatterns = [
    path(
        'auth/login',
        obtain_jwt_token,
        name = 'obtain_jwt_token'
    ),
    path(
        'menus',
        menu.MenuList.as_view(),
        name = 'menu_list'
    ),
    path(
        'menus/current-menu',
        menu.CurrentMenu.as_view(),
        name = 'current_menu'
    ),
    path(
        'menus/current-menu/<uuid:uuid>',
        menu.CurrentMenuByUUID.as_view(),
        name = 'current_menu_by_uuid'
    ),
    path(
        'menus/<int:menu_id>',
        menu.MenuDetail.as_view(),
        name = 'menu_detail'
    ),
    path(
        'menus/<int:menu_id>/send-menu',
        menu.SendMenu.as_view(),
        name = 'send_menu'
    ),
    path(
        'menus/<int:menu_id>/meals',
        meal.MealList.as_view(),
        name = 'meal_list'
    ),
    path(
        'menus/<int:menu_id>/meals/<int:meal_id>',
        meal.MealDetail.as_view(),
        name = 'meal_detail'
    ),
    path(
        'menus/<int:menu_id>/meals/<int:meal_id>/orders',
        order.OrderMealList.as_view(),
        name = 'order_list'
    )
]