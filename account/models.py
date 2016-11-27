from django.conf import settings
from django.contrib.auth.models import User
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


class Contact(models.Model):
    # user which created relationship
    user_from = models.ForeignKey(User, related_name='rel_from_set')
    # user being followed
    user_to = models.ForeignKey(User, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


# add the following field to User dynamically
# monkey-patch =/
User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         # if I follow you, it doesn't mean you automatically follow me
                                         symmetrical=False))
