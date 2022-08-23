from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.utils import timezone

from user.models.user import User
from user.models.otp import OTP
from user.serializers.serializers import UserSerializer
from user.utils.utils import SendSMS, create_end_time, randN, end_time
from user.tasks import send_sms_celery

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

    def post(self, request):
        user = get_object_or_404(User, phone_number=request.data['phone_number'])
        otp_obj = OTP.objects.filter(user=user)
        if otp_obj:
            otp_obj = OTP.objects.get(user=user)
            count_otp = otp_obj.number_error_code5
            if count_otp < 5:
                otp_obj.code = randN(6)
                otp_obj.exp_time = create_end_time()
                otp_obj.exp_time_error1 = end_time()
                otp_obj.number_error_code5 = count_otp + 1
                otp_obj.save()
                send_sms_celery(phone=user.phone_number, code=otp_obj.code, type=2)
                return (Response(otp_obj.code, status=status.HTTP_200_OK))
            else:
                if otp_obj.exp_time_error1 < timezone.now():
                    otp_obj.code = randN(6)
                    otp_obj.exp_time = create_end_time()
                    otp_obj.exp_time_error1 = end_time()
                    otp_obj.number_error_code5 = count_otp + 1
                    otp_obj.save()
                    send_sms_celery(phone=user.phone_number, code=otp_obj.code, type=2)
                    return (Response(otp_obj.code, status=status.HTTP_200_OK))
                else:
                    return(Response('Try again an hour', status=status.HTTP_429_TOO_MANY_REQUESTS))
        else:
            otp_obj = OTP.objects.create(
                    code=randN(6),
                    exp_time=create_end_time(),
                    exp_time_error1=end_time(),
                    user=user,
                    type=2,
                    number_error_code3=0,
                    exp_time_error2=None,
                    number_error_code5=1
            )
            send_sms_celery(phone=user.phone_number, code=otp_obj.code, type=2)
            return (Response(otp_obj.code, status=status.HTTP_200_OK))
        '''
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
        '''


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
        obj = OTP.objects.filter(user=user)
        count_otp = obj.number_error_code5
        if count_otp <= 5:
            otp_obj = OTP.objects.create(
                code=randN(6),
                exp_time=create_end_time(),
                exp_time_error1=end_time(),
                user=user,
                type=2,
                number_error_code=0,
                exp_time_error2=None,
                number_error_code5=count_otp + 1
            )
            x.send_sms(phone=user.phone_number, code=otp_obj.code, type=2)
            return (Response(otp_obj.code, status=status.HTTP_200_OK))
        else:
            otp_obj = OTP.objects.filter(user=user)
            if otp_obj.exp_time_error1 < timezone.now():
                otp_obj.code = randN(6)
                otp_obj.exp_time = create_end_time()
                otp_obj.exp_time_error1 = end_time()
                otp_obj.number_error_code5 = count_otp + 1
                otp_obj.save()
                x.send_sms(phone=user.phone_number, code=otp_obj.code, type=2)
                return (Response(otp_obj.code, status=status.HTTP_200_OK))
            else:
                return(Response('Try again an hour', status=status.HTTP_401_UNAUTHORIZED))


class VerifiedAPI(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def post(self, request):
        user = get_object_or_404(User, phone_number=request.data['phone_number'])
        otp = OTP.objects.get(user=user)
        serializer = self.get_serializer(user)
        token, created = Token.objects.get_or_create(user=user)
        if otp.number_error_code3 > 3:
            if otp.exp_time_error2 > timezone.now():
                return(Response('Try again an hour', status=status.HTTP_401_UNAUTHORIZED))
            else:
                otp.number_error_code3 = 0
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
                    otp.number_error_code3 += 1
                    return(Response('incorrect code', status=status.HTTP_401_UNAUTHORIZED))
            else:
                return(Response('use the new code', status=status.HTTP_401_UNAUTHORIZED))



