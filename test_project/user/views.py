import email
import json
from multiprocessing import context
import requests
from pathlib import Path

from rest_framework import generics,status
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

from user.models import User,OTP
from user.utils.utils import SendSMS,create_end_time,randN
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
        user = get_object_or_404(User,phone_number=request.data['phone_number'])
        opt_obj = OTP.objects.create(code = randN(6), exp_time = create_end_time(), user = user, type = 2)
        x= SendSMS()
        x.send_sms(phone=user.phone_number,code=opt_obj.code,type = 2)
        return (Response(opt_obj.code,status=status.HTTP_200_OK))


class RegisterAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = False
        user.save()
        opt_obj = OTP.objects.create(code = randN(6),exp_time = create_end_time(),user = user,type = 1)
        x= SendSMS()
        x.send_sms(user.phone_number,opt_obj.code,type = 1)
        return(Response(opt_obj.code,status=status.HTTP_200_OK))


class VerifiedAPI(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def post(self, request):
        user = get_object_or_404(User,phone_number=request.data['phone_number'])
        otp = get_object_or_404(OTP,user=user)
        serializer = self.get_serializer(user)
        token, created = Token.objects.get_or_create(user=user)
        if timezone.now() < otp.exp_time and otp.code == request.data['code']:
            user.is_active = True
            user.save()
            otp.delete()
            context =(token.key,serializer.data)
            return(Response(context,status=status.HTTP_200_OK))
        else:
            return(Response(status=status.HTTP_401_UNAUTHORIZED))


        
        

