from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Message(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    submit_date = models.DateTimeField('date created')
