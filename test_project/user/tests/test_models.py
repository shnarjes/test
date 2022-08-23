from django.test import TestCase

from user.models.user import User
from user.models.otp import OTP
from user.utils.utils import create_end_time_token, create_end_time, end_time


class UserTest(TestCase):

    def setUp(self):
        return User.objects.create(
            first_name='narjes',
            last_name='sh',
            phone_number='09132826759'
        )

    def test_user_creation(self):
        user = User.objects.get(phone_number='09132826759')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), user.phone_number)


class OTPTest(TestCase):

    def setUp(self):
        user = User.objects.create(
            first_name='narjes',
            last_name='sh',
            phone_number='09132826756'
        )
        return OTP.objects.create(
            code='123456',
            exp_time=create_end_time_token(),
            exp_time_error1=create_end_time(),
            exp_time_error2=end_time(),
            user=user,
            type=1,
            number_error_code3=0,
            number_error_code5=0
        )

    def test_OTP_creation(self):
        otp = OTP.objects.get(code='123456')
        self.assertTrue(isinstance(otp, OTP))
        self.assertEqual(otp.__str__(), otp.code)
