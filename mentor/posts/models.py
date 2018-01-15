from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import datetime

# Create your models here.


class UserProfilePost(models.Model):
    poster = models.ForeignKey(User, related_name="posting_user")
    message = models.CharField(max_length=255, default="")
    post_time = datetime.datetime.now


class UserPrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sending_user")
    receiver = models.ForeignKey(User, related_name="receiving_user")
    message = models.TextField()
