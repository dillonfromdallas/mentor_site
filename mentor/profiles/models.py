from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserManager(models.Manager):
    def is_following(self, other_user):
        return Follow.objects.get(follower=self.request.user,
                                  followee=User.objects.get(username=other_user)).exists()

    def is_blocked(self, other_user):
        return Block.objects.get(blocker=self.request.user,
                                 blocked=User.objects.get(username=other_user)).exists()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to="profile_image", blank=True)
    bio = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following')
    followee = models.ForeignKey(User, related_name='followers')

    def __str__(self):
        return f"{self.follower} is following {self.followee}."


class Block(models.Model):
    blocker = models.ForeignKey(User, related_name='blocking')
    blocked = models.ForeignKey(User, related_name='blocked')

    def __str__(self):
        return f"{self.blocked} has been blocked by {self.blocker}."
