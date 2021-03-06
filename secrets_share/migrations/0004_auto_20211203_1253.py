# Generated by Django 3.2.9 on 2021-12-03 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secrets_share', '0003_alter_message_submit_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_encrypted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='submit_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date created'),
        ),
    ]
