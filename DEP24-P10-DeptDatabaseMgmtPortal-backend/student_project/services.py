from .models import StudentProject
from .serializers import *
from basemodel.services import BaseServices,BaseDraftServices
from .access import StudentProjectAccessSpecifier
from .notification_manager import *

class StudentProjectServices(BaseServices):
    model = StudentProject
    serializer = StudentProjectSerializer
    list_serializer = StudentProjectSerializer
    access = StudentProjectAccessSpecifier()
    notification_manager = StudentProjectNotificationManager

    def get_object_emails(self, id):
        obj = self.model.allobjects.get(id = id)
        lis = [obj.mentor]
        for user in obj.members.all():
            lis.append(user)
        return lis

class StudentProjectDraftServices(BaseDraftServices):
    model = StudentProject
    serializer = StudentProjectDraftSerializer
    list_serializer = StudentProjectDraftSerializer
    updateserializer = StudentProjectDraftUpdateSerializer
    access = StudentProjectAccessSpecifier()
    notification_manager = StudentProjectNotificationManager

    def get_object_emails(self, id):
        obj = self.model.allobjects.get(id = id)
        lis = [obj.mentor]
        for user in obj.members.all():
            lis.append(user)
        return lis