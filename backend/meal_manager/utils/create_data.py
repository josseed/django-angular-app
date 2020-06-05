from meal_manager.models import User

def create_nora_user():
    try:
        user = User.objects.filter(email = 'nora@mail.io')
        if not user.exists():
            user = User.objects.create_superuser(
                first_name = "Nora",
                last_name = "Chef",
                email = "nora@mail.io",
                password = "nora"
            )
            print('user nora created.')    
    except BaseException:
        print('creation user nora failed.')