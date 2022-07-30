# Generated by Django 4.0.6 on 2022-07-28 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0002_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='user',
            field=models.ForeignKey(blank=True, help_text='user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratetocustomer', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='commentme',
            name='product',
            field=models.ForeignKey(help_text='product', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commenttoproduct', to='product.product', verbose_name='product'),
        ),
        migrations.AddField(
            model_name='commentme',
            name='user',
            field=models.ForeignKey(blank=True, help_text='user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commenttouser', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
