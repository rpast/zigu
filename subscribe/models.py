from django.db import models
from PIL import Image
from temple.models import God
from django.core.validators import MaxValueValidator, MinValueValidator
# To create user model import module below
from django.contrib.auth.models import User


# Create your models here.

# Additional user information model goes here:
class UserProfileInfo(models.Model):
    # Create this relationship instead of inheriting from User
    # because it can screw up your database
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional fields added in a form of class instances
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics',)

    gods_associated = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])

    gods_created = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])


    # In case you want to print the user
    def __str__(self):
        return self.user.username

    # Override class' default save method
    # We want to customize th save behavior to resize image
    def save(self):
        # Run save method of parent class by using super()
        super().save()

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)




