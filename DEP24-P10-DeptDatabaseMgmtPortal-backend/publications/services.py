from .models import Publication
from .serializers import *
from basemodel.services import BaseServices,BaseDraftServices
from .access import PublicationAccessSpecifier
from .notification_manager import *

class PublicationServices(BaseServices):
    model = Publication
    serializer = PublicationSerializer
    list_serializer = PublicationListSerializer
    access = PublicationAccessSpecifier()
    notification_manager = PublicationNotificationManager

    def get_object_emails(self, id):
        lis = []
        obj = self.model.allobjects.get(id = id)
        for user in obj.authors.all():
            lis.append(user)
        return lis

class PublicationDraftServices(BaseDraftServices):
    model = Publication
    serializer = PublicationDraftSerializer
    list_serializer = PublicationListSerializer
    updateserializer = PublicationDraftUpdateSerializer
    access = PublicationAccessSpecifier()
    notification_manager = PublicationNotificationManager

    def get_object_emails(self, id):
        lis = []
        obj = self.model.allobjects.get(id = id)
        for user in obj.authors.all():
            lis.append(user)
        return lis