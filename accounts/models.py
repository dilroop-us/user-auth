from django.contrib.auth.models import User

class CustomUser(User):


    def __str__(self):
        return self.username