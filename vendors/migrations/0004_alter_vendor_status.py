# Generated by Django 4.2.7 on 2023-11-29 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0003_remove_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='status',
            field=models.CharField(blank=True, choices=[('Fulfilled', 'Fulfilled')], max_length=50, null=True),
        ),
    ]
