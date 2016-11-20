from django.conf import settings
from django.db import models


# Django also offers a way to substitute the whole User model with your own custom
# model. Your user class should inherit from Django's AbstractUser class, which
# provides the full implementation of the default user as an abstract model. You can
# read more about this method at
# https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#substituting-a-custom-user-model

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

