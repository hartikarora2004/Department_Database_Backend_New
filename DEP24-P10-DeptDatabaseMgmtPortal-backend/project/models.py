from django.db import models
from basemodel.models import BaseModel
from usercustom.models import CustomUser
from department.models import Department
from django.core.exceptions import ValidationError
# Create your models here.

class Project(BaseModel):

    class ProjectStatus(models.TextChoices):
        ONGOING = 'ON', "ONGOING"
        COMPLETED = 'CO', "COMPLETED"
        CANCELLED = 'CA', "CANCELLED"

    title = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=5, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    members = models.ManyToManyField(CustomUser, related_name='%(class)s_members')
    investors = models.TextField(null=True, blank=True)
    amount_invested = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=ProjectStatus.choices, default=ProjectStatus.ONGOING)

    def __str__(self):
        return self.title
    
    class Meta:
        constraints = [models.CheckConstraint(check=~(models.Q(is_draft=True) & models.Q(is_approved=True)), name='projec draft cannot be approved'),
                       models.UniqueConstraint(fields=['draft_id', 'is_approved', 'is_deleted'], condition=models.Q(is_approved=False) & models.Q(is_deleted = False), name='Only one project draft can be made for each object'),
                       models.UniqueConstraint(fields=['code', 'is_approved'], condition= models.Q(is_deleted = False), name="project_code_is_unique"),
                    ]
        
class ProjectEditHistory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='edit_history')
    editor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name= self.editor.first_name + ' ' + self.editor.last_name
        edited_date = self.edited_at.date()  # Extract only the date part
        return f"{self.project.title} edited by {name} on {edited_date}"