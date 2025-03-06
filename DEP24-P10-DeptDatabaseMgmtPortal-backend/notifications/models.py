from django.db import models
from usercustom.models import CustomUser
# Create your models here.
# import django user groups
from django.contrib.auth.models import Group


class baseNotification(models.Model):
    notification = models.TextField(null=True, blank=True, max_length=100)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    redirect_link = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.notification
    
    class Meta:
        abstract = True


class userNotifications(baseNotification):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_user')


    

class broadcastNotifications(baseNotification):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_group')
    expiry_time = models.DateTimeField(null=True, blank=True)
    department = models.ForeignKey('department.Department', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_department')