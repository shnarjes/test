from django.urls import path

from product.views import ProductAddView

app_name = "product"
urlpatterns = [
    path('addproduct', ProductAddView.as_view(), name='addproduct'),
]
