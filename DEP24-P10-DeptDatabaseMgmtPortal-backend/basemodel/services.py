from .models import BaseModel
from .serializers import *
from .access import *
from .notification_manager import *
from usercustom.models import CustomUser
class BaseServices():
    model = BaseModel
    serializer = BaseSerializer
    list_serializer = BaseSerializer
    access = BaseAccessSpecifier()
    notification_manager = BaseNotificationManager

    def get_object_emails(self, id):
        return []

    # gets all required objects
    def get_list(self, **kwargs):
        """
        Returns all objects of the model
        args: kwargs
        return: status(bool), objects(list)
        """
        return self.model.objects.filter(**kwargs)
    
    def get_user_list(self, **kwargs):
        """
        Returns all objects of the user
        args: kwargs
        return: status(bool), objects(list)
        """
        try:
            obj = self.list_serializer(self.model.objects.filter(**kwargs),many = True)
            return True,obj
        except Exception as e:
            return False,str(e)

    # gets a particular object for internal use
    def get_object(self, id):
        """
        Returns a particular object of the model
        args: id
        return: object(Django model object)
        """
        return self.model.objects.get(id = id)

    # create new object
    def create(self, request):
        """
        Creates a new object of the model
        args: request
        return: status(bool), object(Django model object)
        """
        notify = self.notification_manager(request.user, request)
        serializer = self.serializer(data = request.data, context = {'request':request})
        if serializer.is_valid():
            try:
                serializer.save()
                print('a')
                notify.mailing_list = self.get_object_emails(serializer.data['id'])
                notify.create_post(serializer)
                return True,serializer
            except Exception as e:
                return False,str(e)
        return False, serializer.errors
    
    # gets a particular object service
    def get(self, id):
        """
        Returns a particular object of the model
        args: id
        return: status(bool), serialized object(DRF serializer object)/errors
        """
        try:
            serializer = self.serializer(self.model.objects.get(id = id))
        except Exception as e:
            return False,self.model.__name__ + " not found"
        return True,serializer
    
    # update object details
    def update(self, id, request):
        """
        Updates a particular object of the model
        args: id, request
        return: status(bool), serialized object(DRF serializer object)/errors
        """
        notify = self.notification_manager(request.user, request)
        notify.mailing_list = self.get_object_emails(id)
        try:
            serializer = self.serializer(self.model.objects.get(id = id),data = request.data, context = {'request':request})
        except Exception as e:
            return False,self.model.__name__ + " not found"
        if serializer.is_valid():
            try:
                serializer.save()
                notify.mailing_list += self.get_object_emails(serializer.data['id'])
                notify.id_put(id, serializer)
                return True,serializer
            except Exception as e:
                return False,str(e)
        return False,serializer.errors

    # delete object
    def delete(self, id, request):
        """
        Deletes a particular object of the model
        args: id, request
        return: status(bool), message(string)/errors
        """
        notify = self.notification_manager(request.user, request)
        notify.mailing_list = self.get_object_emails(id)
        try:
            serializer = self.serializer(self.model.objects.get(id = id), context = {'request':request})
        except Exception as e:
            return False,self.model.__name__ + " not found"
        try:
            serializer.delete()
            notify.id_delete(id, serializer)
            return True,"Successfully deleted"
        except Exception as e:
            return False,str(e)

    def get_deleted_obj(self, id):
        """
        Returns a particular deleted object of the model
        args: id
        return: status(bool), serialized object(DRF serializer object)/errors
        """
        try:
            serializer = self.serializer(self.model.deleted.get(id = id))
        except Exception as e:
            return False,self.model.__name__ + " not found"
        return True,serializer

    # restore object
    def restore(self, id, request):
        """
        Restores a particular deleted object of the model
        args: id, request
        return: status(bool), serialized object(DRF serializer object)/errors
        """
        notify = self.notification_manager(request.user, request)
        notify.mailing_list = self.get_object_emails(id)
        try:
            obj = self.model.allobjects.get(id = id)
            serializer = self.serializer(obj, context = {'request':request})
        except Exception as e:
            return False,self.model.__name__ + " not found"
        if obj.is_deleted == False:
            return False,"Object is not deleted"
        try:
            obj.save()
        except Exception as e:
            return False,str(e)
        serializer.restore(obj)
        notify.restore_id_put(id, serializer)
        return True,serializer

    def get_deleted(self, request, **kwargs):
        """
        Returns all deleted objects of the model
        args: kwargs(to filter queryset)
        return: status(bool), serialized objects(DRF serializer object)/errors
        """
        try:
            return True,self.list_serializer(self.model.deleted.filter(**kwargs),many = True)
        except Exception as e:
            return False,str(e)

    
class BaseDraftServices():
    """
        Base class for all services related to draft objects
         
    """
    model = BaseModel
    serializer = BaseDraftSerializer
    list_serializer = BaseDraftSerializer
    updateserializer = BaseDraftUpdateSerializer
    access = BaseAccessSpecifier()
    notification_manager = BaseNotificationManager

    def get_object_emails(self, id):
            return []

    def get_drafts(self, request, **kwargs):
        try:
            return True,self.list_serializer(self.model.drafts.filter(**kwargs),many = True)
        except Exception as e:
            return False,str(e)

    def create_draft(self, request):
        try:
            ser = self.serializer(data =  request.data, context = {'request':request})
            if ser.is_valid():
                ser.save()
                return True,ser
            else:
                return False,ser.errors
        except Exception as e:
            return False,str(e)
    
    def create_previous_draft(self, id, request):
        try:
            serializer = self.serializer(self.model.objects.get(id = id),data = request.data, context = {'request':request})
        except Exception as e:
            print(e)
            return False,self.model.__name__ + " not found"
        if serializer.is_valid():
            try:
                serializer.save()
                return True,serializer
            except Exception as e:
                return False,str(e)
        return False,serializer.errors
    
    def get_draft(self, id):
        try:
            serializer = self.serializer(self.model.drafts.get(id = id))
        except Exception as e:
            return False,self.model.__name__ + " not found"
        return True,serializer
    
    def update_draft(self, id, request):
        try:
            obj = self.model.drafts.get(id = id)
            print(obj)
            try:
                ser = self.updateserializer(obj,data = request.data, context = {'request':request})
                print("updating")
                if ser.is_valid():
                    ser.save()
                    return True,ser
                else:
                    return False,ser.errors
            except Exception as e:
                return False,str(e)
        except Exception as e:
            return False,self.model.__name__ + " not found"
        
    def delete_draft(self, id, request):
        try:
            obj = self.model.drafts.get(id = id)
            try:
                obj.delete_draft()
            except Exception as e:
                return False,str(e)
            return True,None
        except Exception as e:
            return False,self.model.__name__ + " not found"
    
    def submit(self, id, request):
        self.access.set_user(request.user)
        notify = self.notification_manager(request.user, request)
        notify.mailing_list = self.get_object_emails(id)
        if(self.access.can_approve(id)):
            print("can approve")
            return self.approve(id, request)
        try:
            obj = self.model.drafts.get(id = id)
            try:
                obj.submit_draft()
            except Exception as e:
                return False,str(e)
            ser = self.serializer(obj)
            notify.submit_id_put(id, ser)
            return True,ser
        except Exception as e:
            print('error')
            print(e)
            return False,self.model.__name__ + " not found"

    def get_pending_obj(self, id):
        try:
            serializer = self.serializer(self.model.pending.get(id = id))
        except Exception as e:
            return False,self.model.__name__ + " not found"
        return True,serializer

    def approve(self, id, request):
        notify = self.notification_manager(request.user, request)
        notify.mailing_list = self.get_object_emails(id)
        try:
            obj = self.model.nonapproved.get(id = id)
            try:
                obj.approve(self.model)
            except Exception as e:
                return False,str(e)
            ser = self.serializer(obj)
            notify.approve_id_put(id, ser)
            return True,ser
        except Exception as e:
            print('not found')
            print(e)
            return False,self.model.__name__ + " not found"
        
    def reject(self, id, request):
        notify = self.notification_manager(request.user, request)
        notify.mailing_list = self.get_object_emails(id)
        try:
            obj = self.model.nondeleted.get(id = id)
            try:
                obj.reject()
            except Exception as e:
                return False,str(e)
            ser = self.serializer(obj)
            notify.reject_id_put(id, ser)
            return True,ser
        except Exception as e:
            return False,self.model.__name__ + " not found"

    def get_pending(self, request, kwargs1,kwargs2):
        print('get pending')
        try:
            list1 = self.model.pending.filter(**kwargs1).distinct()
            list2 = self.model.pending.filter(**kwargs2).distinct()
            list3 = (list1 | list2).distinct()
            return True,self.list_serializer(list3,many = True)
        except Exception as e:
            return False,str(e)


def process_data(key,value,datatypes):
    if datatypes[key] == 'int':
        if value == None or value == '':
            return None
        return int(value)
    elif datatypes[key] == 'float':
        if value == None or value == '':
            return None
        return float(value)
    elif datatypes[key] == 'list':
        if value == None or value == '':
            return None
        return [int(i) for i in value.split(';')]
    elif datatypes[key] == 'list_str':
        if value == None or value == '':
            return None
        return value.split(';')
    elif datatypes[key] == 'string':
        if value == None or value == '':
            return None
        return value.replace(';',',')
    elif datatypes[key] == 'dd-mm-yyyy':
        if value == None or value == '':
            return None
        return f"{value[6:]}-{value[3:5]}-{value[:2]}"
    elif datatypes[key] == 'email':
        if value == None or value == '':
            return None
        try:
            usr = CustomUser.objects.get(email = value)
            return usr.id
        except Exception as e:
            raise Exception('Email not found in database')
    elif datatypes[key] == 'email_list':
        if value == None or value == '':
            return None
        email_list = []
        for email in value.split(';'):
            try:
                usr = CustomUser.objects.get(email = email)
                email_list.append(usr.id)
            except Exception as e:
                raise Exception(f'Email {email} not found in database. Please remove it from the list and try again')
        return email_list
    else:
        raise Exception('Invalid datatype in datatype row')

def preprocess(data):
    if data == None:
        raise Exception('No data found')
    if 'id' in data:
        del data['id']
    if 'created_by' in data:
        del data['created_by']
    if 'created_at' in data:
        del data['created_at']
    return data

def add_model(row,datatypes,request,ser):
    data = {}
    print("adding data\n\n\n\n\n\n\n")
    for key, value in row.items():
        print(key,value)
        data[key] = process_data(key,value,datatypes)
        print("processed data", data[key])
    preprocess(data)
    print("preprocessed data", data)
    serializer = ser(data = data, context = {'request':request})
    print("serializer", serializer)
    if serializer.is_valid():
        print("valid")
        serializer.save()
        print("success")
        return serializer.data, None
    else:
        return  None, serializer.errors