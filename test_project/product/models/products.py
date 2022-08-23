from django.db import models
from django.urls import reverse
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from product.models.category import Category
from product.models.color import Color


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Please select your product name."),
        verbose_name=_('product name')
    )
    image = models.ImageField(
        upload_to="Products",
        null=True, blank=True,
        help_text=_("upload your image"),
        verbose_name=_('image')
    )
    image1 = models.ImageField(
        upload_to="Products",
        null=True,
        blank=True,
        help_text=_("upload your image"),
        verbose_name=_('image')
    )
    image2 = models.ImageField(
        upload_to="Products",
        null=True, blank=True,
        help_text=_("upload your image"),
        verbose_name=_('image')
    )
    price = models.PositiveIntegerField(
        verbose_name=_('price'),
        help_text=_("Enter the product price")
    )
    capacity = models.PositiveIntegerField(
        verbose_name=_('capacity'),
        help_text=_("product inventory")
    )
    discription = models.TextField(
        verbose_name=_('discription'),
        help_text=_("Relevant descriptions"),
        null=True,
        blank=True
    )
    color = models.ManyToManyField(
        Color,
        help_text=_("Choose the color of your product"),
        )
    brand = models.CharField(
        max_length=16,
        null=True,
        help_text=_("Enter your product brand"),
    )
    cat = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        related_name="producttocat",
        help_text=_("category")
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
        help_text=_("date")
        )
    data_update = models.DateTimeField(
        auto_now=True,
        help_text=_("date update")
        )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        return self.name

    @property
    def return_category(self):
        category = Category.objects.get(pk=self.cat.id)
        return category

    def get_absolute_url(self):
        return reverse('Product:product_detail', args=[self.id])

    def save(self, *args, **kwargs):
        key = "product" + str(self.id)
        cache.delete(key)
        cache.delete('product')
        return super(Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        key = "product" + str(self.id)
        cache.delete(key)
        cache.delete('product')
        return super(Product, self).delete(*args, **kwargs)
