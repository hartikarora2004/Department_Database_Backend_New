from .models import Visit
from .serializers import *
from basemodel.services import BaseServices,BaseDraftServices
from .access import VisitAccessSpecifier
from .notification_manager import *

class VisitServices(BaseServices):
    model = Visit
    serializer = VisitSerializer
    list_serializer = VisitListSerializer
    access = VisitAccessSpecifier()
    notification_manager = VisitNotificationManager

    def get_object_emails(self, id):
        obj = self.model.allobjects.get(id = id)
        lis = [obj.user]
        return lis

class VisitDraftServices(BaseDraftServices):
    model = Visit
    serializer = VisitDraftSerializer
    list_serializer = VisitListSerializer
    updateserializer = VisitDraftUpdateSerializer
    access = VisitAccessSpecifier()
    notification_manager = VisitNotificationManager

    def get_object_emails(self, id):
        obj = self.model.allobjects.get(id = id)
        lis = [obj.user]
        return lis