from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        _('Phone Number'),
        max_length=11,
        unique=True,
        null=True,
        blank=True
    )
    email = models.EmailField(
        null=True,
        blank=True
    )
    objects = UserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone_number)

   

'''
class Address(models.Model):
    add = models.CharField(
        max_length=255,
        verbose_name=("address"),
        help_text=_("Enter your Address")
    )
    postalcode = models.CharField(
        max_length=10,
        verbose_name=_("postalcode"),
        help_text=_("Enter your postalcode"),
        null=True,
        blank=True
    )
    user = models.ManyToManyField(
        User,
        help_text=_("user"),
        blank=True
        )

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.add

'''
