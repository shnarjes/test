from django.contrib import admin

from product.models.products import Product
from product.models.category import Category
from product.models.color import Color


admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Product)
