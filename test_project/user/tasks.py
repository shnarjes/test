from celery import shared_task

from user.utils.utils import SendSMS


@shared_task
def send_sms_celery(phone, code, type):
    s = SendSMS()
    s.send_sms(phone=phone, code=code, type=type)
