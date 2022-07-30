from django.contrib import admin

from notification.models import notif_user, News


admin.site.register(notif_user)
admin.site.register(News)
