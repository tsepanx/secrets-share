import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser
from core import settings

from .encryption import encrypt, decrypt


class User(AbstractUser):
    pass


class Message(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    submit_date = models.DateTimeField('Date created', auto_now_add=True)
    # is_encrypted = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, **kwargs):
        password = kwargs.get('password', None)
        if password:
            self.text = encrypt(self.text, password)

        super().save(force_insert, force_update, using, update_fields)

    def get_hash_id(self):
        id_string = str(self.id)
        # salt = 'my_salt'
        salt = settings.SECRET_KEY

        h = hashlib.sha256(id_string.encode())
        h.update(salt.encode())

        return h.hexdigest()

    def get_decrypted_text(self, password):
        return decrypt(self.text, password)

    def __str__(self):
        return f'{self.title}, {self.text}'
