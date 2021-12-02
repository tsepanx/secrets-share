import hashlib

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser

from core import settings


class User(AbstractUser):
    pass


class Message(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    submit_date = models.DateTimeField('date created', auto_now_add=True)

    def get_hash_id(self):
        id_string = str(self.id)
        # salt = 'my_salt'
        salt = settings.SECRET_KEY

        h = hashlib.sha256(id_string.encode())
        h.update(salt.encode())

        return h.hexdigest()

    def __str__(self):
        return f'{self.title}, {self.text}'
