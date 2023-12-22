from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import random
from django.dispatch import Signal
from twilio.rest import Client

# Custom Signals
pre_create = Signal()


# This class sent otp for user through twilio 
class otp_message_handler:
    mobile_number = None

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def sent_otp(self):
        verify_sid = "VA39917fe21ae0ea9b18dbc89454242a9a"
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        verification = client.verify.v2.services(verify_sid) \
        .verifications \
        .create(to='+91'+self.phone_number, channel="sms")

    def check_otp(self, otp_code):
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        verify_sid = "VA39917fe21ae0ea9b18dbc89454242a9a"
        verification_check = client.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to='+91'+self.phone_number, code=otp_code)
        print("-------------------")
        return verification_check.valid

        



@receiver(pre_create)
def pre_create_handler(sender, instance, **kwargs):
    if not instance.user_id:
        message_obj = otp_message_handler(instance.phone_number)
        message_obj.sent_otp()

