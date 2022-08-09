from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from numpy import number
from user.managers import UserManager


class OTPType(models.IntegerChoices):
    REGISTER = (1, _("REGISTER"))
    LOGIN = (2, _("LOGIN"))


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        _('Phone Number'),
        max_length=11,
        unique=True,
        null=True,
        blank=True
    )
    objects = UserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return str(self.phone_number)


class OTP(models.Model):
    code = models.CharField(
        max_length=11,
        verbose_name=_("code"),
        help_text=_("code"),
        unique=True
        )
    exp_time = models.DateTimeField(
        verbose_name=_("exp_time"),
        help_text=_("Time out")
        )
    exp_time_error1 = models.DateTimeField(
        verbose_name=_("exp_time_error"),
        help_text=_("Time out"),
        null=True,
        blank=True
        )
    exp_time_error2 = models.DateTimeField(
        verbose_name=_("exp_time_error"),
        help_text=_("Time out"),
        null=True,
        blank=True
        )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="otp_user",
        verbose_name=_("user"),
        help_text=_("user")
        )
    type = models.IntegerField(
        choices=OTPType.choices,
        verbose_name=_("type"),
        help_text=_("type")
        )
    number_error_code = models.PositiveIntegerField(
        verbose_name=_("number_error_code"),
        help_text=_("number_error_code"),
        null=True,
        blank=True
    )

    @property
    def is_expired(self):
        if self.exp_time < timezone.now():
            return True
        return False

    def __str__(self):
        return self.code


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
