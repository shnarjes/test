from django.contrib import admin

from product.models import (
    Category,
    Color,
    Product,
    WishList,
    Property,
    Details,
)


admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(WishList)
admin.site.register(Property)
admin.site.register(Details)
