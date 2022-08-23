from rest_framework import routers

from product.views.views import ProductAPIViewSet


app_name = "product"
router = routers.SimpleRouter()
router.register('products', ProductAPIViewSet, basename='product')
urlpatterns = router.urls
