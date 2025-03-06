from .models import Event
from .serializers import *
from basemodel.services import BaseServices,BaseDraftServices
from .access import EventAccessSpecifier
from .notification_manager import *

class EventServices(BaseServices):
    model = Event
    serializer = EventSerializer
    list_serializer = EventListSerializer
    access = EventAccessSpecifier()
    notification_manager = EventNotificationManager

    def get_object_emails(self, id):
        lis = []
        obj = self.model.allobjects.get(id = id)
        for user in obj.organizers.all():
            lis.append(user)
        return lis

class EventDraftServices(BaseDraftServices):
    model = Event
    serializer = EventDraftSerializer
    list_serializer = EventListSerializer
    updateserializer = EventDraftUpdateSerializer
    access = EventAccessSpecifier()
    notification_manager = EventNotificationManager

    def get_object_emails(self, id):
        lis = []
        obj = self.model.allobjects.get(id = id)
        for user in obj.organizers.all():
            lis.append(user)
        return lis