from meal_manager.models import Order, Worker, Meal, Menu
from datetime import date 

def create_order(order_dict: dict):
    """ 
    this function create the order of a meal.

    expected order_dict = {
        'worker_id': value, - required
        'meal_position': value, - int required
        'customization': value - optional
    }

    the steps are the following:
    1) check the order_data.
    2) get the worker by worker_id.
    3) get the menu for the current day.
    4) get the meal of the menu by position.
    5) get the previus order if exists.
    5) update or create the order.
    return a boolean with the result
    """

    #checking keys 
    if not order_dict.get('worker_id'):
        raise Exception('worker_id is required in order_dict')
    if not order_dict.get('meal_position'):
        raise Exception('meal_position is required in order_dict')
    if not isinstance(order_dict.get('meal_position'), int):
        raise Exception('meal_position value must be a number.') 

    #get worker
    try:
        worker = Worker.objects.get(pk = order_dict.get('worker_id'))
    except Worker.DoesNotExist:
        return False
    
    #get the current menu
    try:
        today = date.today().strftime("%Y-%m-%d")
        menu = Menu.objects.get(date = today)
    except Menu.DoesNotExist:
        return False
    
    #get the meal of the menu by position
    try:
        meals = menu.meals.all()
        meal = meals[order_dict.get('meal_position') -1]
    except BaseException:
        return False
    
    previus_order = False
    #check if a previus order exist.
    try:
        order = Order.objects.get(
            worker_id = worker.id,
            date = today,
        )
        previus_order = True
    except Order.DoesNotExist:
        pass
    
    #update or create the order
    try:
        if previus_order:
            order.meal_id = meal.id
            order.customization = order_dict.get('customization')
            order.save()
        else:
            Order.objects.create(
                worker_id = worker.id,
                meal_id = meal.id,
                date = today,
                customization = order_dict.get('customization')
            )
    except BaseException:
        return False
    
    return True
    