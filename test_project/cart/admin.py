from django.contrib import admin

from cart.models import CartMe, CartItem, History


admin.site.register(CartMe)
admin.site.register(CartItem)
admin.site.register(History)
