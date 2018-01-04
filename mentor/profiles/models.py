from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # Note: Add max file size limit.
    avatar = models.ImageField(upload_to="pic_folder/",
                               default="pic_folder/default_profile_picture_all.jpg")
    bio = models.CharField(max_length=255, default="")


# First get the UserProfile model going, then add in django-friendship
