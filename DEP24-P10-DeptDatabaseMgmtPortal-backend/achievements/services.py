from .models import Achievement
from .serializers import *
from basemodel.services import BaseServices,BaseDraftServices
from .access import AchievementAccessSpecifier
from .notification_manager import *

class AchievementServices(BaseServices):
    model = Achievement
    serializer = AchievementSerializer
    list_serializer = AchievementListSerializer
    access = AchievementAccessSpecifier()
    notification_manager = AchievementNotificationManager

    def get_object_emails(self, id):
        lis = []
        obj = self.model.allobjects.get(id = id)
        for user in obj.participants.all():
            lis.append(user)
        return lis

class AchievementDraftServices(BaseDraftServices):
    model = Achievement
    serializer = AchievementDraftSerializer
    list_serializer = AchievementListSerializer
    updateserializer = AchievementDraftUpdateSerializer
    access = AchievementAccessSpecifier()
    notification_manager = AchievementNotificationManager

    def get_object_emails(self, id):
        lis = []
        obj = self.model.allobjects.get(id = id)
        for user in obj.participants.all():
            lis.append(user)
        return lis