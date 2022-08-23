from django.db import models
from django.utils.translation import gettext_lazy as _


class Color(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Choose the color of your product"),
        verbose_name=_('color')
    )

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self) -> str:
        return self.title
