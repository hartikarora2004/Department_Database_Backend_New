from django.db import models
from basemodel.models import BaseModel
from usercustom.models import CustomUser
from department.models import Department
# Create your models here.

class Visit(BaseModel):
    class VisitType(models.TextChoices):
        LECTURE  = 'LC', 'Lecture'
        CONFERENCE = 'CF', 'Conference'
        SEMINAR = 'SM', 'Seminar'
        OTHER = 'O', 'Other'

    
    title = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(class)s_authors')
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    venue = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=2, choices=VisitType.choices, default=VisitType.LECTURE)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [models.CheckConstraint(check=~(models.Q(is_draft=True) & models.Q(is_approved=True)), name='Visit draft cannot be approved'),
                       models.UniqueConstraint(fields=['draft_id', 'is_approved', 'is_deleted'], condition=models.Q(is_approved=False) & models.Q(is_deleted = False), name='Only one Visit draft can be made for each object'),
                    ]

class VisitEditHistory(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='edit_history')
    editor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name= self.editor.first_name + ' ' + self.editor.last_name
        edited_date = self.edited_at.date()  # Extract only the date part
        return f"{self.visit.title} edited by {name} on {edited_date}"