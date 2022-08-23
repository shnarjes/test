from rest_framework import status
from datetime import timedelta

from django.urls import reverse
from django.test import TestCase
from django.test.utils import override_settings

from user.models.user import User
from user.models.otp import OTP


class APITest(TestCase):

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def setUp(self):
        User.objects.create(
            first_name='narjes',
            last_name='sh',
            phone_number='09903198644'
        )

    def test_error_code5(self):
        user = User.objects.get(phone_number='09903198644')
        signin_dict = {
            'phone_number': user.phone_number
        }
        for i in range(6):
            response = self.client.post(reverse('user:login'), signin_dict)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_accept_code5(self):
        user = User.objects.get(phone_number='09903198644')
        signin_dict = {
            'phone_number': user.phone_number
        }
        for i in range(4):
            response = self.client.post(reverse('user:login'), signin_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accept_code_1hour(self):
        user = User.objects.get(phone_number='09903198644')
        signin_dict = {
            'phone_number': user.phone_number
        }

        for i in range(6):
            response = self.client.post(reverse('user:login'), signin_dict)
        obj_otp = OTP.objects.get(user=user)
        obj_otp.exp_time_error1 = obj_otp.exp_time_error1 - timedelta(minutes=65)
        obj_otp.save()
        response = self.client.post(reverse('user:login'), signin_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_object_otp(self):
        user = User.objects.get(phone_number='09903198644')
        signin_dict = {
            'phone_number': user.phone_number
        }
        response = self.client.post(reverse('user:login'), signin_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
