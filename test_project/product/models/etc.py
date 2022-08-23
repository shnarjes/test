'''
from django.db import models
from django.urls import reverse
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from user.models.user import User
class WishList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlisttocustomer",
        help_text=_("user"),
        null=True,
        blank=True
    )
    product = models.ManyToManyField(
        Product,
        help_text=_("product")
    )
    datetime = models.DateTimeField(
        auto_now=True,
        verbose_name=_('date and time'),
        help_text=_("data and time")
    )

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

    def __str__(self) -> str:
        return self.user.email


class Property(models.Model):
    property_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text=_("property name")
    )
    cat_id = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='propertytocat',
        help_text=_("category")
    )

    def __str__(self) -> str:
        return self.property_name


class Details(models.Model):
    pro_id = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='detailstoproperty',
        help_text=_("property"),
        null=True
    )
    product_id = models.ManyToManyField(Product)
    detail = models.CharField(
        max_length=400,
        help_text=_("product"),
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return self.detail

'''
