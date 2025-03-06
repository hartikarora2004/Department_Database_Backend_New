from django.db import models

class NonDeleted(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class Deleted(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = True)

class Approved(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_approved = True).filter(is_deleted = False)
    
class Drafts(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_draft = True).filter(is_deleted = False)
    
class Pending(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_approved = False).filter(is_deleted = False).filter(is_draft = False).filter(object_type = 'P')

class NonApproved(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_approved = False).filter(is_deleted = False)