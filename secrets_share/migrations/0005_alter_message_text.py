# Generated by Django 3.2.9 on 2021-12-03 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secrets_share', '0004_auto_20211203_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(max_length=100000),
        ),
    ]
