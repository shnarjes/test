from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = routers.SimpleRouter()
schema_view = get_schema_view(
    openapi.Info(
        title="INCOME EXPENSES API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="contact@expenses.local"),
        license=openapi.License(name="Test License")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),
    path('api/', include('product.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/clearcache/', include('clearcache.urls')),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    # path('api/cart/', include('cart.urls')),
    # path('api/comment/', include('comment.urls')),
    # path('api/introduction/', include('introduction.urls')),
    # path('api/notification/', include('notification.urls')),
    # path('api/payment/', include('payment.urls')),
]
