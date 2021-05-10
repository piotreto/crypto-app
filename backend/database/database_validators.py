from database.models import User
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth.hashers import make_password, check_password

def checkIfUserExists(user_name):
    user = User.objects.filter(email = user_name)
    return len(user) > 0
    

def checkIfPasswordMatches(user_name, user_password):
    user = User.objects.get(email = user_name)
    return check_password(user_password, user.password)

def validateEmail(email="sedziborow..$$"):
    try:
        valid = validate_email(email)
        return True

    except EmailNotValidError:
        return False
        

    