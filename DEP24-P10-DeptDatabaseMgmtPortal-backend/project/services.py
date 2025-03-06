from .models import Project
from .serializers import *
from basemodel.services import BaseServices,BaseDraftServices
from .access import ProjectAccessSpecifier
from .notification_manager import *

class ProjectServices(BaseServices):
    model = Project
    serializer = ProjectSerializer
    list_serializer = ProjectListSerializer
    access = ProjectAccessSpecifier()
    notification_manager = ProjectNotificationManager

    def get_object_emails(self, id):
        lis = []
        obj = self.model.allobjects.get(id = id)
        for user in obj.members.all():
            lis.append(user)
        return lis

class ProjectDraftServices(BaseDraftServices):
    model = Project
    serializer = ProjectDraftSerializer
    list_serializer = ProjectListSerializer
    updateserializer = ProjectDraftUpdateSerializer
    access = ProjectAccessSpecifier()
    notification_manager = ProjectNotificationManager

    def get_object_emails(self, id):
        lis = []
        obj = self.model.allobjects.get(id = id)
        for user in obj.members.all():
            lis.append(user)
        return lis