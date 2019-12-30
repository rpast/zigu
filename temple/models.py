from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image

# Create your models here.


class God(models.Model):
    name = models.CharField(max_length=500)
    god_description = models.TextField(max_length=2500)

    blessing_name = models.CharField(max_length=250)
    blessing_description = models.TextField(max_length=1000)

    profile_pic = models.ImageField(default='default_god.jpg', upload_to='pantheon_pics',)

    followers = models.ManyToManyField(User, blank=True)

    # Dont know why this one breaks the database column :/
    #cultists = models.ManyToManyField(User, blank=True)
    #cultists = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    # cultists_number = models.IntegerField(
    #     default=0,
    #     validators=[
    #         MinValueValidator(0),
    #         MaxValueValidator(50),
    #     ]
    # )

    sacrum = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )

    shaping = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )

    vortex = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )

    # In case you want to print the user
    def __str__(self):
        return self.name


    def save(self):
        # Run save method of parent class by using super()
        super().save()

        img = Image.open(self.profile_pic.path)

        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size, Image.LANCZOS)
            img.save(self.profile_pic.path)