# Generated by Django 4.0.6 on 2022-08-21 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_otp_number_error_code3_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Address',
        ),
    ]
