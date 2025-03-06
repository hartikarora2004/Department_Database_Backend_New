from django.db import models
from basemodel.models import BaseModel
from usercustom.models import CustomUser
from department.models import Department
# Create your models here.

class Event(BaseModel):
    class EventType(models.TextChoices):
        WORKSHOP = 'WS', 'Workshop'
        CONFERENCE = 'CF', 'Conference'
        SEMINAR = 'SM', 'Seminar'
        INVITED_LECTURES = 'IL', 'Invited Lectures'
        OTHER = 'O', 'Other'

    
    title = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=2, choices=EventType.choices, default=EventType.OTHER)
    date = models.DateField(null=True, blank=True)
    venue = models.TextField(null=True, blank=True)
    organizers = models.ManyToManyField(CustomUser, related_name='%(class)s_authors', blank=True)
    speakers = models.TextField(null=True, blank=True)
    number_of_participants = models.IntegerField(null=True, blank=True,default = 0)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [models.CheckConstraint(check=~(models.Q(is_draft=True) & models.Q(is_approved=True)), name='Event draft cannot be approved'),
                       models.UniqueConstraint(fields=['draft_id', 'is_approved', 'is_deleted'], condition=models.Q(is_approved=False) & models.Q(is_deleted = False), name='Only one Event draft can be made for each object'),
                    ]

class EventEditHistory(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='edit_history')
    editor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name= self.editor.first_name + ' ' + self.editor.last_name
        edited_date = self.edited_at.date()  # Extract only the date part
        return f"{self.event.title} edited by {name} on {edited_date}"