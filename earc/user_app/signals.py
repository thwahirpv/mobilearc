from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import random
from django.dispatch import Signal
from admin_app import models 
from django.core.exceptions import ObjectDoesNotExist


# Custom Signals
pre_create = Signal()

class otp_message_handler:
    def generate_opt(self):
        return random.randint(100000, 999999)  
    
    # sent otp given email
    def sent_otp(self, email, otp):
        subject = 'Mobilearc OTP verification'
        message = f"Don't share the otp anyone our team don't ask your ONE-TIME-PASSWORD (otp) we take your security very serious. OTP: {otp}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
     
    # check otp 
    def check_otp(self, otp, entered_otp):
        if otp == entered_otp:
            return True
        else:
            return False
          
# create_user signal    
@receiver(pre_create)
def pre_create_handler(sender, instance, **kwargs):
    otp_obj = otp_message_handler() 
    otp = otp_obj.generate_opt()
    instance.otp = otp
    instance.save()
    otp_obj.sent_otp(instance.email, otp)
    
    

