# Generated by Django 4.2.7 on 2023-11-29 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
