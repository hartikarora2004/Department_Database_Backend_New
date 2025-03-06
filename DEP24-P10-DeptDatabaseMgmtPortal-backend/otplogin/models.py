from django.db import models
import datetime
import random
import string
# Create your models here
from django.core.mail import send_mail
from usercustom.models import CustomUser
# from zoneinfo import ZoneInfo
import pytz

# # models.py
# from django.db import models
# from django.contrib.auth.models import User

# class Publication(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     last_edit_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     last_edit_date = models.DateTimeField(auto_now=True)

# class EditHistory(models.Model):
#     publication = models.ForeignKey(Publication, related_name='edit_history', on_delete=models.CASCADE)
#     edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     edit_date = models.DateTimeField(auto_now_add=True)

class Otpdetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6,blank=True,null=True)
    time = models.DateTimeField(blank=True,null=True)
    link_string = models.CharField(max_length=20,blank=True,null=True)
    is_active = models.BooleanField(default=True)

    def setup(self,*args, **kwargs):
        self.time = datetime.datetime.now()
        self.otp = str(random.randint(234567,999999))
        self.link_string = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase +string.digits, k=20))
        print( 'Please find your otp below :' + str(self.otp))
        if self.user.get_otp_email:
            print(send_mail('Welcome to DEP', 'Please find your otp below :' + str(self.otp), 'donotreplydepartmentdata@gmail.com', [self.user.email], fail_silently=False))
    
    def is_valid_link(self):
        current_time = datetime.datetime.now()
        current_time = current_time.replace(tzinfo=datetime.timezone.utc)
        difference = current_time - self.time 
        min = difference.total_seconds()/60
        if min>=15:
            return False
        else:
            return True and self.is_active
    
    def is_valid_otp(self,otp):
        print("ṭ")
        current_time = datetime.datetime.now()
        # set indian timezone
        tz = pytz.timezone('Asia/Kolkata')
        current_time = tz.localize(current_time)
        otp_time = self.time
        difference = current_time - otp_time 
        min = difference.total_seconds()/60
        print(min)
        if min>=2:
            return False
        else:
            return True and ((str(otp) == self.otp) and self.is_active)
