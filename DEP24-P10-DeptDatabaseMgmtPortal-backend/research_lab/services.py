from basemodel.services import BaseServices
from .models import ResearchLab
from .serializers import ResearchLabSerializer
from .notification_manager import *

class ResearchLabServices(BaseServices):
    model = ResearchLab
    serializer = ResearchLabSerializer
    notification_manager = ResearchLabNotificationManager

    def get_object_emails(self, id):
        lis = []
        obj = self.model.allobjects.get(id = id)
        for user in [obj.Head]:
            lis.append(user)
        return lis