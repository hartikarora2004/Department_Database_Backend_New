from notifications.email_notification import email_notification
from .serializers import *
from .models import *
from .htmlgenerator import *



class BaseNotificationManager:
    user = None
    request = None
    model = BaseModel
    mailing_list = []

    def __init__(self,user,request):
        self.user = user
        self.request = request


    def user_get(self, serializer):
        pass

    def create_post(self, serializer):
        try:
            subject = "New " + self.model.__name__ + " created by " + self.user.username + " with id " + str(serializer.data['id'])
            message = f"New {self.model.__name__} created with id {str(serializer.data['id'])} by {self.user.username} \n\n object data : \n\n {init_html_table(serializer.data)}"
            email_notification(self.mailing_list,subject, message, self.user, True)
        except Exception as e:
            print(e)
        self.mailing_list = []

    def id_get(self, id, serializer):
        pass

    def id_put(self, id, serializer):
        try:
            subject = self.model.__name__ + " object updated by " + self.user.username + " with id " + str(serializer.data['id'])
            message = f"{self.model.__name__} with id {str(serializer.data['id'])} updated by {self.user.username} \n\n new object data : \n\n {init_html_table(serializer.data)}"
            email_notification(self.mailing_list,subject, message, self.user, True)
        except Exception as e:
            print(e)
        self.mailing_list = []
    
    def id_delete(self, id, serializer):
        try:
            obj = self.model.allobjects.get(id = id)
            subject = self.model.__name__ + " deleted by " + self.user.username + " with id " + str(id)
            message = self.model.__name__ + " deleted with id " + str(id) + " by " + self.user.username
            email_notification(self.mailing_list,subject, message, obj.created_by, True)
        except Exception as e:
            print(e)
        self.mailing_list = []
    
    def restore_id_get(self, id, serializer):
        pass

    def restore_id_put(self, id, serializer):
        try:
            obj = self.model.allobjects.get(id = id)
            subject = self.model.__name__ + " restored by " + self.user.username + " with id " + str(id)
            message = self.model.__name__ + " restored with id " + str(id) + " by " + self.user.username
            email_notification(self.mailing_list,subject, message, obj.created_by,True)
        except Exception as e:
            print(e)
        self.mailing_list = []

    def draft_get(self, serializer):
        pass

    def draft_post(self, serializer):
        pass

    def draft_id_get(self, id, serializer):
        pass

    def draft_id_put(self, id, serializer):
        pass

    def draft_id_delete(self, id, serializer):
        pass
    
    def draft_id_post(self, id, serializer):
        pass

    def submit_id_put(self, id, serializer):
        try:
            obj = self.model.allobjects.get(id = serializer.data['id'])
            subject = self.model.__name__ + " submitted for approval by " + self.user.username + " with id " + str(serializer.data['id'])
            message = f"An {self.model.__name__} with id {str(serializer.data['id'])} submitted for approval by {self.user.username} \n\n object data : \n\n {init_html_table(serializer.data)}"
            email_notification(self.mailing_list,subject, message, obj.created_by,True)
        except Exception as e:
            print(e)
        self.mailing_list = []

    def approve_id_get(self, id, serializer):
        pass

    def approve_id_put(self, id, serializer):
        try:
            obj = self.model.allobjects.get(id = serializer.data['id']) 
            subject = self.model.__name__ + " approved by " + self.user.username + " with id " + str(serializer.data['id'])
            message = self.model.__name__ + " approved with id " + str(id) + " by " + self.user.username
            message+= "\n\nobject data : \n\n" + init_html_table(serializer.data)
            email_notification(self.mailing_list, subject, message, obj.created_by,True)
        except Exception as e:
            print(e)
        self.mailing_list = []

    def reject_id_put(self, id, serializer):
        try:
            obj = self.model.allobjects.get(id = serializer.data['id'])
            subject = self.model.__name__ + " rejected by " + self.user.username + " with id " + str(serializer.data['id'])
            message = self.model.__name__ + " rejected with id " + str(id) + " by " + self.user.username
            message+= "\n\nobject data : \n\n" + init_html_table(serializer.data)
            email_notification(self.mailing_list,subject, message, obj.created_by,True)
        except Exception as e:
            print(e)
        self.mailing_list = []

    def pending_get(self, serializer):
        pass

    def deleted_get(self, serializer):
        pass
    