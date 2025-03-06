from notifications.email_notification import email_notification
from .serializers import *
from .models import *
from basemodel.notification_manager import BaseNotificationManager



class ResearchLabNotificationManager(BaseNotificationManager):
    model = ResearchLab
