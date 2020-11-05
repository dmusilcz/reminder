from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.


class Profile(models.Model):
    choices = settings.LANGUAGES
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(choices=choices,
                                default=settings.LANGUAGE_CODE,
                                max_length=2)
    news_consent = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_language_display(self):
        return self.choices.get(self.language)[1]
