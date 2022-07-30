from django.contrib import admin
from django.urls import path, include

from rest_framework import routers


router = routers.SimpleRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/product/', include('product.urls')),
    # path('api/cart/', include('cart.urls')),
    # path('api/comment/', include('comment.urls')),
    # path('api/introduction/', include('introduction.urls')),
    # path('api/notification/', include('notification.urls')),
    # path('api/payment/', include('payment.urls')),
]
