import email
import json
import requests
from pathlib import Path

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404
from django.utils import timezone
from yaml import serialize

from user.models import User, OTP
from user.utils.utils import SendSMS, create_end_time, randN, end_time
from user.serializers import UserSerializer

'''
class LoginAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = LoginSerializer

    def get_object(self):
        return self.request.user


class RegisterAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })
'''


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        x = SendSMS()
        user = get_object_or_404(User, phone_number=request.data['phone_number'])
        otp_count = OTP.objects.filter(user=user).count()
        if otp_count <= 5:
            otp_obj = OTP.objects.create(
                code=randN(6),
                exp_time=create_end_time(),
                exp_time_error1=end_time(),
                user=user,
                type=2,
                number_error_code=0,
                exp_time_error2=None
            )
            x.send_sms(phone=user.phone_number, code=otp_obj.code, type=2)
            return (Response(otp_obj.code, status=status.HTTP_200_OK))
        else:
            otp_obj = OTP.objects.filter(user=user).last()
            if otp_obj.exp_time_error < timezone.now():
                delete_obj = OTP.objects.filter(user=user).delete()
                otp_obj = OTP.objects.create(
                    code=randN(6),
                    exp_time=create_end_time(),
                    exp_time_error1=end_time(),
                    user=user,
                    type=2,
                    number_error_code=0,
                    exp_time_error2=None
                )
                x.send_sms(phone=user.phone_number, code=otp_obj.code, type=2)
                return (Response(otp_obj.code, status=status.HTTP_200_OK))
            else:
                return(Response('Try again an hour', status=status.HTTP_401_UNAUTHORIZED))


class RegisterAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def post(self, request):
        x = SendSMS()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = False
        user.save()
        otp_count = OTP.objects.filter(user=user).count()
        if otp_count <= 5:
            otp_obj = OTP.objects.create(
                code=randN(6),
                exp_time=create_end_time(),
                exp_time_error1=end_time(),
                user=user,
                type=2,
                number_error_code=0,
                exp_time_error2=None
            )
            x.send_sms(phone=user.phone_number, code=otp_obj.code, type=2)
            return (Response(otp_obj.code, status=status.HTTP_200_OK))
        else:
            otp_obj = OTP.objects.filter(user=user).last()
            if otp_obj.exp_time_error < timezone.now():
                delete_obj = OTP.objects.filter(user=user).delete()
                otp_obj = OTP.objects.create(
                    code=randN(6),
                    exp_time=create_end_time(),
                    exp_time_error1=end_time(),
                    user=user,
                    type=2,
                    number_error_code=0,
                    exp_time_error2=None
                )
                x.send_sms(phone=user.phone_number, code=otp_obj.code, type=2)
                return (Response(otp_obj.code, status=status.HTTP_200_OK))
            else:
                return(Response('Try again an hour', status=status.HTTP_401_UNAUTHORIZED))


class VerifiedAPI(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def post(self, request):
        breakpoint()
        user = get_object_or_404(User, phone_number=request.data['phone_number'])
        otp = OTP.objects.filter(user=user).last()
        serializer = self.get_serializer(user)
        token, created = Token.objects.get_or_create(user=user)
        if otp.number_error_code > 3:
            if otp.exp_time_error2 > timezone.now():
                return(Response('Try again an hour', status=status.HTTP_401_UNAUTHORIZED))
            else:
                otp.number_error_code = 0
                return(Response('use the new code', status=status.HTTP_401_UNAUTHORIZED))
        else:
            if timezone.now() < otp.exp_time:
                if otp.code == request.data['code']:
                    user.is_active = True
                    user.save()
                    otp.delete()
                    context = (token.key, serializer.data)
                    return(Response(context, status=status.HTTP_200_OK))
                else:
                    otp.number_error_code += 1
                    return(Response('incorrect code', status=status.HTTP_401_UNAUTHORIZED))
            else:
                return(Response('use the new code', status=status.HTTP_401_UNAUTHORIZED))
