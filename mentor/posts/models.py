from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import datetime

# Create your models here.


class UserProfilePost(models.Model):
    poster = models.ForeignKey(User, related_name="posting_user")
    profile = models.ForeignKey(User, related_name="to_post_profile")
    message = models.CharField(max_length=255, default="")
    post_time = datetime.datetime.now  # This doesnt quite work.

    def __str__(self):
        if self.poster == self.profile:
            return f"{self.poster} posted on their profile."
        else:
            return f"{self.poster} posted on {self.profile}'s profile."


class UserPrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sending_user")
    receiver = models.ForeignKey(User, related_name="receiving_user")
    message = models.TextField()
