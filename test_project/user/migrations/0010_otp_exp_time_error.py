# Generated by Django 4.0.6 on 2022-08-09 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_otp_exp_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='exp_time_error',
            field=models.DateTimeField(blank=True, help_text='Time out', null=True, verbose_name='exp_time_error'),
        ),
    ]
