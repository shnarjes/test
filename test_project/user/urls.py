from django.urls import path, include
# from django.views.generic import TemplateView
# from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views.views import LoginAPIView, RegisterAPIView, VerifiedAPI

app_name = "user"
urlpatterns = [
    # path('', TemplateView.as_view(template_name="index.html")),
    # path('accounts/', include('allauth.urls')),
    # path('logout', LogoutView.as_view()),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('register', RegisterAPIView.as_view(), name='register'),
    path('verified', VerifiedAPI.as_view(), name='varified'),
]
