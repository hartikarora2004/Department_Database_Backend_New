from basemodel.access import BaseAccessSpecifier
from .models import StudentProject

# class StudentProjectAccessSpecifier(BaseAccessSpecifier):
#     model = StudentProject
    
#     def check_staff(self):
#         return self.user.groups.filter(name='Staff').exists()

#     def can_get_user_list(self):
#         if self.user is not None:
#             return True,{'members':self.user}
#         return False,{}
    
#     def can_create(self):
#         if super().can_create():
#             return True
#         return self.user.groups.filter(name='Faculty').exists()


#     def can_update(self, StudentProject):
#         StudentProject = self.get_object(StudentProject)
#         if StudentProject == None:
#             return False
#         if(super().can_update(StudentProject.id)):
#             return True
#         return self.user == StudentProject.mentor


#     def can_view_draft_list(self):
#         return True,{'created_by': self.user}
    
#     def can_create_draft(self):
#         return True

#     def can_create_previous_draft(self,id):
#         StudentProject = self.get_object(id)
#         if StudentProject == None:
#             return False
#         if(super().can_create_previous_draft(StudentProject)):
#             return True
#         if self.user == StudentProject.mentor:
#             return True
#         if self.user == StudentProject.created_by:
#             return True
#         return self.user in StudentProject.members.all()
    
#     def can_view_draft(self, id):
#         StudentProject = self.get_object(id)
#         if StudentProject == None:
#             return False
#         if(super().can_create_previous_draft(StudentProject)):
#             return True
#         if self.user == StudentProject.created_by:
#             return True
#         return False
    
#     def can_update_draft(self, id):
#         return self.can_view_draft(id)
    
#     def can_delete_draft(self, id):
#         return self.can_view_draft(id)
        
#     def can_submit_draft(self, id):
#         return self.can_view_draft(id)
    
#     def can_view_pending(self, id):
#         return self.can_create_previous_draft(id)
    
#     def can_approve(self, id):
#         return self.can_update(id)
    
#     def can_reject(self, id):
#         return self.can_update(id)
    
#     def can_view_pending_list(self):
#         if self.check_staff():
#             return True,{}
#         if self.user.groups.filter(name='Faculty').exists():
#             return True,{'mentor':self.user}
#         return True, {'members':self.user}
    


class StudentProjectAccessSpecifier(BaseAccessSpecifier):
    model = StudentProject

    def object_user(self, obj):
        lis =  [obj.created_by]
        patrs = obj.members.all()
        for patr in patrs:
            lis.append(patr)
        return lis
    
    def get_heads(self, obj):
        lis = [obj.mentor]
        return lis

    
    def get_object_owner_filter(self):
        return {'members': self.user}
    
    def get_object_fa_filter(self):
        return {'mentor': self.user}