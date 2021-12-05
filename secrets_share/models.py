import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser
from core import settings

from .encryption import encrypt, decrypt


class User(AbstractUser):
    pass


class Message(models.Model):
    HASH_ID_SIZE = 8

    text = models.TextField(max_length=10 ** 5)
    submit_date = models.DateTimeField('Date created', auto_now_add=True)
    is_encrypted = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, **kwargs):
        password = kwargs.get('password', None)

        if password:
            self.text = encrypt(self.text, password)
            self.is_encrypted = True
        else:
            self.is_encrypted = False

        super().save(force_insert, force_update, using, update_fields)

    def get_hash_id(self):
        """
        Get a hash string from Model primary key, and limit its length with Message.HASH_ID_SIZE
        """

        id_string = str(self.id)
        salt = settings.SECRET_KEY

        h = hashlib.sha256(id_string.encode())
        h.update(salt.encode())

        hash_string = h.hexdigest()
        return hash_string[:Message.HASH_ID_SIZE + 1]

    def get_decrypted_text(self, password):
        return decrypt(self.text, password)

    def __str__(self):
        return f'{self.text}'
