from basemodel.access import BaseAccessSpecifier
from .models import Project

# class ProjectAccessSpecifier(BaseAccessSpecifier):
#     model = Project
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

#     def can_update(self, Project):
#         Project = self.get_object(Project)
#         if Project == None:
#             return False
#         if(super().can_update(Project.id)):
#             return True
#         return self.user in Project.members.all()


#     def can_view_draft_list(self):
#         return True,{'created_by': self.user}
    
#     def can_create_draft(self):
#         return self.can_create()

#     def can_create_previous_draft(self,id):
#         Project = self.get_object(id)
#         if Project == None:
#             return False
#         if(super().can_create_previous_draft(Project)):
#             return True
#         return self.user in Project.members.all()
    
#     def can_view_draft(self, id):
#         Project = self.get_object(id)
#         if Project == None:
#             return False
#         if(super().can_create_previous_draft(Project)):
#             return True
#         if self.user == Project.created_by:
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
#         return True, {'members':self.user}


class ProjectAccessSpecifier(BaseAccessSpecifier):
    model = Project

    def object_user(self, obj):
        lis =  [obj.created_by]
        patrs = obj.members.all()
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
        return {'members': self.user}
    
    def get_object_fa_filter(self):
        return {'members__student_details__faculty_advisor': self.user}