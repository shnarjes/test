from django.urls import path

from rest_framework import routers

from product.views import ProductAddView, ProductAPIViewSet

app_name = "product"
router = routers.SimpleRouter()
router.register('products', ProductAPIViewSet, basename='productview')
urlpatterns = [
    path('addproduct', ProductAddView.as_view(), name='addproduct'),

] + router.urls
