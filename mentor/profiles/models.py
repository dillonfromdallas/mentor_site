from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Create your models here.


class UserModelExtension(User):

    def is_following(self, other_user):
        try:
            other_username = User.objects.get(username=other_user)
            test = Follow.objects.get(follower=self.username, followee=other_username)
            return True
        except ObjectDoesNotExist:
            return False

    class Meta:
        proxy = True


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # Note: Add max file size limit.
    avatar = models.ImageField(upload_to="pic_folder/",
                               default="pic_folder/default_profile_picture_all.jpg")
    bio = models.CharField(max_length=255, default="")


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following')
    followee = models.ForeignKey(User, related_name='followers')
