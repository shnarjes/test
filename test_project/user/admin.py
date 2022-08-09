from django.contrib import admin

from user.models import User, Address,OTP


admin.site.register(OTP)
admin.site.register(User)
admin.site.register(Address)
