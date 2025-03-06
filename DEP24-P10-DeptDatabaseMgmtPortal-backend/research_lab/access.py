from basemodel.access import BaseAccessSpecifier
from .models import ResearchLab

# class ResearchLabAccessSpecifier(BaseAccessSpecifier):
#     model = ResearchLab

#     def check_hod(self):
#         return self.user.groups.filter(name='Research_lab_head').exists()

#     def can_get_user_list(self):
#         if self.check_hod():
#             return True, {'Head': self.user}
#         return False, {}


class ResearchLabAccessSpecifier(BaseAccessSpecifier):
    model = ResearchLab

    def object_user(self, obj):
        lis =  [obj.created_by,obj.Head]
        return lis

    def get_heads(self, obj):
        return self.object_user(obj)
    
    def get_object_owner_filter(self):
        return {'Head': self.user}
    
    def get_object_fa_filter(self):
        return {'Head': self.user}
    
    def can_create(self):
        return self.user.groups.filter(name='Staff').exists()
    