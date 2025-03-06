from django.db import models
from usercustom.models import CustomUser
from .manager import NonDeleted, Deleted, Approved, Drafts, Pending, NonApproved
import datetime

class BaseModel(models.Model):
    class object_status(models.TextChoices):
        DRAFT = 'DR', ('Draft')
        PENDING = 'P', ('Pending')
        ACTIVE = 'A', ('Active')
        REJECTED = 'R', ('Rejected')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by  = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_deleted_by')
    is_deleted = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    draft_id = models.IntegerField(null=True, blank=True)
    object_type = models.CharField(max_length=2, choices=object_status.choices, default=object_status.ACTIVE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_created_by')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_creator')
    department = models.ManyToManyField('department.Department', related_name='%(class)s_department', blank=True)
    users = models.CharField(max_length=500, null=True, blank=True)
    tags = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        abstract = True
        constraints = [models.CheckConstraint(check=~models.Q(is_draft=True) & models.Q(is_approved=True), name='is_draft_is_approved'),
                       models.UniqueConstraint(fields=['draft_id', 'is_approved', 'is_deleted'], condition=models.Q(is_approved=False) & models.Q(is_deleted = False), name='unique_draft_for_object')
                       ]

    allobjects = models.Manager()
    objects = Approved()
    pending = Pending()
    drafts = Drafts()
    nondeleted  = NonDeleted()
    deleted = Deleted()
    nonapproved = NonApproved()

    def soft_delete(self,user):
        self.is_deleted = True
        self.deleted_at = datetime.datetime.now()
        self.deleted_by = user
        super(BaseModel, self).save()

    def restore(self):
        self.is_deleted = False
        self.save()

    # def create_draft(self, cls):
    #     print(self.__dict__)
    #     draft = cls.objects.create(**self.__dict__)
    #     draft.object_type = self.object_status.DRAFT
    #     draft.is_draft = True
    #     draft.is_approved = False
    #     draft.draft_id = self.id
    #     draft.save()
    #     return draft
    
    @classmethod
    def create_new_draft(cls,**kwargs):
        draft = cls.objects.create(**kwargs)
        draft.object_type = BaseModel.object_status.DRAFT
        draft.is_draft = True
        draft.is_approved = False
        draft.draft_id = None
        draft.save()
        return draft

    def update_draft(self, **kwargs):
        self.__dict__.update(**kwargs)
        self.save()
        return self

    def submit_draft(self):
        self.is_draft = False
        self.object_type = self.object_status.PENDING
        self.is_approved = False
        self.save()
        return self
    
    def delete_draft(self):
        self.delete()
        return True

    def approve(self,cls):
        if(self.draft_id != None):
            try:
                obj = cls.objects.get(id = self.draft_id)
                dict_values = self.__dict__.copy()
                dict_values['id'] = self.draft_id
                dict_values['draft_id'] = None
                self.is_deleted = True
                self.save()
                obj.__dict__.update(**dict_values)
                obj.is_draft = False
                obj.is_approved = True
                obj.object_type = obj.object_status.ACTIVE
                obj.draft_id = obj.id
                print("hello saving obj")
                obj.save()
                return 
            except cls.DoesNotExist:
                pass
        self.draft_id = None
        self.is_deleted = False
        self.is_draft = False
        self.is_approved = True
        self.object_type = self.object_status.ACTIVE
        self.save()
    
    def reject(self):
        self.object_type = self.object_status.REJECTED
        self.is_draft = False
        self.is_approved = False
        self.save()
    
    def delete_object_drafts(self,cls):
        cls.nonapproved.filter(draft_id = self.id).delete()