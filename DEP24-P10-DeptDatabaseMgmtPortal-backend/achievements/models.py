from django.db import models
from basemodel.models import BaseModel
from usercustom.models import CustomUser
# Create your models here.

class Achievement(BaseModel):
    class AchievementType(models.TextChoices):
        Hackthon = 'HC', 'Hackthon'
        Competition = 'CP', 'Competition'
        Internship = 'IN', 'Internship'
        OTHER = 'O', 'Other'

    
    title = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=2, choices=AchievementType.choices, default=AchievementType.OTHER)
    date = models.DateField(null=True, blank=True)
    participants = models.ManyToManyField(CustomUser, related_name='%(class)s_authors')
    participants_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [models.CheckConstraint(check=~(models.Q(is_draft=True) & models.Q(is_approved=True)), name='Achievement draft cannot be approved'),
                       models.UniqueConstraint(fields=['draft_id', 'is_approved', 'is_deleted'], condition=models.Q(is_approved=False) & models.Q(is_deleted = False), name='Only one Achievement draft can be made for each object'),
                    ]

class AchievementEditHistory(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='edit_history')
    editor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name= self.editor.first_name + ' ' + self.editor.last_name
        edited_date = self.edited_at.date()  # Extract only the date part
        return f"{self.achievement.title} edited by {name} on {edited_date}"