from base64 import decode
import os
import json
import random
import requests

from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone

STATUS_CHOICES ={
    'register':'Your verification code for register: ',
    'login':'Your verification code for login: ',
}
   

class SendSMS():
    
    UserApiKey = "e2ea1cb9c4f48f84d0fe1079"
    SecretKey = "27XB2Fi4nhtNYX1OCHL4am3esOxg_m1uDRLi837r0M8Ooyl0aw"

    def request_token(self):
        url = "https://RestfulSms.com/api/Token"
        data = {"UserApiKey": self.UserApiKey, "SecretKey": self.SecretKey}
        token = requests.post(url, data)
        text_token = token.text
        text_token = json.loads(text_token)
        return text_token["TokenKey"]

    def get_token(self):
        if os.path.exists("user/utils/file.txt"):
            with open("user/utils/file.txt", "r") as file:
                token_key = file.readline()
                end_time = file.readline()
                end_time = datetime.strptime(end_time, '%d/%m/%y %H:%M:%S')
                if datetime.now() > end_time :
                    return self.write_file()
                else:
                    return str(token_key)
        else:
            return self.write_file()
            

    def send_sms(self, phone, code, type):
        token_key = self.get_token()
        token_key = token_key.replace('\n','')
        if type == 1:
            type_sms = STATUS_CHOICES["register"]
        else:
            type_sms = STATUS_CHOICES["login"]
        code_sms = type_sms + str(code)
        url = "https://RestfulSms.com/api/MessageSend"
        headers = {"x-sms-ir-secure-token": token_key}
        data ={"Messages":[code_sms],"MobileNumbers": [f"{phone}"],"LineNumber": self.get_sms_line()}
        sms = requests.post(url, data, headers=headers)
    
    def request_sms_line(self):
        token_key = self.get_token()
        token_key = token_key.replace('\n','')
        url = "https://RestfulSms.com/api/SMSLine"
        headers ={"x-sms-ir-secure-token": token_key}
        line_sms = requests.get(url, headers=headers)
        line_sms = line_sms.text
        line_number = json.loads(line_sms)
        return line_number['SMSLines'][0]['LineNumber']

    def get_sms_line(self):
        if os.path.exists("user/utils/file2.txt"):
            with open("user/utils/file2.txt", "r") as file:
                sms_line = file.readline()
                return str(sms_line)
        else:
            with open("user/utils/file2.txt", "w") as file:
                sms_line = str(self.request_sms_line())
                return str(sms_line) 

    def write_file(self):
            with open("user/utils/file.txt", "w") as file:
                token_key = self.request_token()
                end_time = create_end_time_token()
                end_time = end_time.strftime('%d/%m/%y %H:%M:%S')
                file.write(token_key)
                file.write("\n")
                file.write(end_time)
                return str(token_key)


def randN(N):
	min = pow(10, N-1)
	max = pow(10, N) - 1
	return random.randint(min, max)

def create_end_time_token():
    return datetime.now() + timedelta(minutes=30)

def create_end_time():
    return timezone.now() + timedelta(minutes=3)

