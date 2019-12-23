from django.db import models
# To create user model import module below
from django.contrib.auth.models import User


# Create your models here.

# Additional user information model goes here:
class UserProfileInfo(models.Model):
    # Create this relationship instead of inheriting from User
    # because it can screw up your database
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional fields added in a form of class instances
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)

    # In case you want to print the user
    def __str__(self):
        return self.user.username
