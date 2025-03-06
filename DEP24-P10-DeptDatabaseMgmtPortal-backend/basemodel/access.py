class BaseAccessSpecifier():
    user = None
    def set_user(self,user):
        self.user = user

    def object_user(self, obj):
        return [obj.created_by]
    
    def get_heads(self, obj):
        if obj.created_by.groups.filter(name='Faculty').exists():
            return [obj.created_by]
        return [obj.created_by.student_details.faculty_advisor]

    def get_object(self, id):
        try:
            return self.model.allobjects.get(id=id)
        except Exception as e:
            return None
    
    def get_object_owner_filter(self):
        return {'created_by': self.user}
    
    def get_object_fa_filter(self):
        return {'created_by__student_details__faculty_advisor': self.user}
    

    def can_list(self):
        if self.user is not None:
            return True
        return False

    def can_get_user_list(self):
        if self.user is not None:
            return True,self.get_object_owner_filter()
        return False,{}
    
    def can_create(self):
        return self.user.groups.filter(name__in=['Faculty', 'Staff']).exists()
    
    def can_view(self, id):
        if self.user is not None:
            return True
        return False
    
    def can_update(self, id):
        if self.user in self.get_heads(self.get_object(id)):
            return True
        return False
    
    def can_delete(self, id):
        if self.user in self.get_heads(self.get_object(id)):
            return True
        return False

    def can_view_deleted(self, id):
        if self.get_object(id).deleted_by == self.user:
            return True
        return False

    def can_restore(self, id):
        if self.get_object(id).deleted_by == self.user:
            return True
        return False

    def can_view_draft_list(self):
        if self.user is not None:
            return True,{'created_by': self.user}
        return False,{}

    def can_create_draft(self):
        return True
    
    def can_create_previous_draft(self, id):
        obj = self.get_object(id)
        if self.user in self.get_heads(obj):
            return True
        if self.user in self.object_user(obj):
            return True
        return False

    def can_view_draft(self, id):
        obj = self.get_object(id)
        if obj.created_by == self.user:
            return True
        return False
    
    def can_update_draft(self, id):
        return self.can_view_draft(id)
    
    def can_delete_draft(self, id):
        return self.can_view_draft(id)
    
    def can_submit_draft(self, id):
        return self.can_view_draft(id)
    
    def can_view_pending(self, id):
        return self.can_create_previous_draft(id)
    
    def can_approve(self, id):
        print("approve status")
        if self.user in self.get_heads(self.get_object(id)):
            return True
        return False
    
    def can_reject(self, id):
        return self.can_approve(id)

    def can_view_pending_list(self):
        if self.user.groups.filter(name='Faculty').exists():
            return True, self.get_object_fa_filter(), self.get_object_owner_filter()
        else:
            return True,self.get_object_owner_filter(), self.get_object_owner_filter()
   
    def can_view_deleted_list(self):
        return True,{'deleted_by': self.user}
    
    def is_staff(self):
        return self.user.groups.filter(name='Staff').exists()