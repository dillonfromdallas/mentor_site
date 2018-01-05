from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Create your models here.


class UserManager(models.Manager):
    def is_following(self, other_user):
        yourself = self.request.user
        other_username = User.objects.get(username=other_user)
        try:
            test = Follow.objects.get(follower=yourself, followee=other_username)
            return True
        except ObjectDoesNotExist:
            return False


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # Note: Add max file size limit.
    avatar = models.ImageField(upload_to="pic_folder/",
                               default="pic_folder/default_profile_picture_all.jpg")
    bio = models.CharField(max_length=255, default="")


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following')
    followee = models.ForeignKey(User, related_name='followers')
