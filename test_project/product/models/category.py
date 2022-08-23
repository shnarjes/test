from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _


class Category(models.Model):

    title = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Please select your product name."),
        verbose_name=_('title')
    )
    category_p = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='catproductmodel',
        verbose_name=_('title'),
        help_text=_("Please select the desired product type"),
        null=True,
        blank=True
    )

    @classmethod
    def get_cat(cls, id):
        get_cat = get_object_or_404(Category, pk=id)
        return get_cat

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.title
