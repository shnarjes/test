# Generated by Django 4.0.6 on 2022-08-03 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
