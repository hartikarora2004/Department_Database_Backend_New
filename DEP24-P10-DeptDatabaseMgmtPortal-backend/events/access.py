from basemodel.access import BaseAccessSpecifier
from .models import Event

# class EventAccessSpecifier(BaseAccessSpecifier):
#     model = Event

#     def check_faculty(self):
#         return self.user.groups.filter(name='Faculty').exists()
    
#     def check_staff(self):
#         return self.user.groups.filter(name='Staff').exists()
    
#     def get_heads(self,object):
#         objs = object.organizers.all()
#         obj_list = []
#         for obj in objs:
#             print(obj)
#             if obj.groups.filter(name='Faculty').exists():
#                 obj_list.append(obj)
#             else:
#                 obj_list.append(obj.student_details.faculty_advisor)
#         return obj_list
    
#     def can_get_user_list(self):
#         if self.user is not None:
#             return True,{'organizers':self.user}
#         return False,{}

#     def can_create(self):
#         if super().can_create():
#             return True
#         return self.user.groups.filter(name='Faculty').exists()

#     def can_update(self, event):
#         event = self.get_object(event)
#         if event == None:
#             return False
#         if(super().can_update(event.id)):
#             return True
#         return self.user in self.get_heads(event)

#     # def can_view_draft_list(self):
#     #     return self.can_create(),{'created_by': self.user}
    
#     def can_create_draft(self):
#         return True

#     def can_create_previous_draft(self,id):
#         event = self.get_object(id)
#         if event == None:
#             return False
#         if(super().can_create_previous_draft(id)):
#             return True
#         if self.user == self.get_heads(event):
#             return True
#         return self.user in event.organizers.all()
    
#     def can_view_draft(self, id):
#         event = self.get_object(id)
#         if event == None:
#             return False
#         if(super().can_create_previous_draft(id)):
#             return True
#         if self.user == event.created_by:
#             return True
#         return False
    
#     def can_update_draft(self, id):
#         return self.can_view_draft(id)
    
#     def can_delete_draft(self, id):
#         return self.can_update_draft(id)
        
#     def can_submit_draft(self, id):
#         return self.can_update_draft(id)
    
#     def can_view_pending(self, id):
#         if self.can_update(id):
#             return True
#         obj = self.get_object(id)
#         if obj == None:
#             return False
#         if self.user == obj.created_by:
#             return True
#         return self.user in obj.organizers.all()
    
#     def can_approve(self, id):
#         return self.can_update(id)
    
#     def can_reject(self, id):
#         return self.can_update(id)

#     def can_view_pending_list(self):
#         if self.can_update(None):
#             return True,{}
#         if self.user.groups.filter(name='Faculty').exists():
#             return True,{'organizers__student_details__faculty_advisor':self.user}
#         return True, {'created_by': self.user}




class EventAccessSpecifier(BaseAccessSpecifier):
    model = Event

    def object_user(self, obj):
        lis =  [obj.created_by]
        patrs = obj.organizers.all()
        for patr in patrs:
            lis.append(patr)
        return lis
    
    def get_heads(self, obj):
        usrs = self.object_user(obj)
        lis = []
        for usr in usrs:
            if usr.groups.filter(name='Faculty').exists():
                lis.append(usr)
            else:
                lis.append(usr.student_details.faculty_advisor)
        return lis

    
    def get_object_owner_filter(self):
        return {'organizers': self.user}
    
    def get_object_fa_filter(self):
        return {'organizers__student_details__faculty_advisor': self.user}