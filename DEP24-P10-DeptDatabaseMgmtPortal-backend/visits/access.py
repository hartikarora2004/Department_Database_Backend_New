from basemodel.access import BaseAccessSpecifier
from .models import Visit

# class VisitAccessSpecifier(BaseAccessSpecifier):
#     model = Visit
# 
    # def can_create(self):
    #     if super().can_create():
    #         return True
    #     return self.user.groups.filter(name='Faculty').exists()

    # def get_head(self, obj):
    #     if obj == None:
    #         return None
    #     if obj.user.groups.filter(name='Faculty').exists():
    #         return obj.user
    #     return obj.user.student_details.faculty_advisor
    
    # def can_update(self, visit):
    #     if super().can_create():
    #         return True
    #     obj = self.get_object(visit)
    #     if obj == None:
    #         return False
    #     return self.user == self.get_head(obj)

    # def can_view_draft_list(self):
    #     return True,{'created_by': self.user}
    
    # def can_create_draft(self):
    #     return True

    # def can_create_previous_draft(self,id):
    #     obj = self.get_object(id)
    #     if obj.user == self.user:
    #         return True
    #     if obj.user == self.get_head(obj):
    #         return True
    #     return False
    
    # def can_view_draft(self, id):
    #     obj = self.get_object(id)
    #     if obj.created_by == self.user:
    #         return True
    #     return False

    # def can_update_draft(self, id):
    #     return self.can_view_draft(id)
    
    # def can_delete_draft(self, id):
    #     return self.can_update_draft(id)
        
    # def can_submit_draft(self, id):
    #     return self.can_update_draft(id)
    
    # def can_view_pending(self, id):
    #     if self.can_update(id):
    #         return True
    #     obj = self.get_object(id)
    #     if obj == None:
    #         return False
    #     if self.user == obj.created_by:
    #         return True
    #     if self.user == obj.user:
    #         return True
    #     return False
    
    # def can_approve(self, id):
    #     return self.can_update(id)
    
    # def can_reject(self, id):
    #     return self.can_update(id)

    # def can_view_pending_list(self):
    #     if self.can_update(None):
    #         return True,{}
    #     if self.user.groups.filter(name='Faculty').exists():
    #         return True,{'user__student_details__faculty_advisor':self.user}
    #     if self.user.groups.filter(name='Student').exists():
    #         return True,{'user':self.user}
    #     return True, {'created_by': self.user}
    
class VisitAccessSpecifier(BaseAccessSpecifier):
    model = Visit

    def object_user(self, obj):
        lis =  [obj.created_by, obj.user]
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
        return {'user': self.user}
    
    def get_object_fa_filter(self):
        return {'user__student_details__faculty_advisor': self.user}
