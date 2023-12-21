from twilio.rest import Client
from django.db.models.signals import pre_save
from django.dispatch import receiver
from admin_app.models import userdetails 
from django.core.mail import send_mail
from django.conf import settings
import random


# This class sent otp for user through twilio 
class otp_message_handler:
    mobile_number = None
    otp = None

    def __init__(self, mobile_number, otp):
        self.mobile_number = mobile_number
        self.otp = otp
        print('3: otp and mobile number save successfully......')

    def sent_otp(self):
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        message = client.messages.create(
                            body=f'To verify your email address, please use the following One Time Password (OTP): {self.otp} Do not share this OTP with anyone. 
                                    mobilearc takes your account security very seriously. 
                                    mobilearc Customer Service will never ask you to disclose or verify your Amazon password, OTP, credit card, 
                                    or banking account number. If you receive a suspicious email with a link to update your account information,
                                    do not click on the link—instead, report the email to mobilearc for investigation.',
                            from_='+15017122661',
                            to='+91'+self.mobile_number
                        )
        print(message.sid)
        print('1: otp sending proccess successfully complete......')
        


def generate_otp():
    print("2: otp generated.....")
    return random.randint(100000, 999999)

# otp pre_save signal its execute before sender model is occer create event
@receiver(pre_save, sender=userdetails)
def sent_otp_to(sender, instance, *args, **kwargs):
    print("the function is woring......")
    # check user_id is not created just for comformation. 
    # once created its means user is alredy created 
    if not instance.user_id:
        print('1: otp sending proccess successfully start......')
        otp = generate_otp()
        instance.otp = otp
        instance.otp.save()
        otp_obj = otp_message_handler(instance.phone_number, otp)
        otp_obj.sent_otp()

