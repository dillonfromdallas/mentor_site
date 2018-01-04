from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    # Note: Add max file size limit.
    avatar = models.ImageField(upload_to="pic_folder/",
                               default="pic_folder/default_profile_picture_all.jpg")
    bio = models.CharField(max_length=255, default="")


