from django.db import models
from usercustom.models import CustomUser
import datetime
# Create your models here.

def get_image_name(instance, filename):
    extension = filename.split('.')[-1]
    current_timestamp = datetime.datetime.now().timestamp()
    fn = f'upload/{current_timestamp}.{extension}'
    return fn


class QueryModel(models.Model):
    class issue_category(models.TextChoices):
        Publications = 'Publications'
        Achievements = 'Achievements'
        Events = 'Events'
        Visits = 'Visits'
        Projects = 'Projects'
        StudentProjects = 'StudentProjects'
        BogReports = 'BogReports'
        DinfoReports = 'DinfoReports'
        Other = 'Other'
    
    class issue_status(models.TextChoices):
        Pending = 'Pending'
        InProgress = 'InProgress'
        Resolved = 'Resolved'
        Rejected = 'Rejected'

    class AssignedTo(models.TextChoices):
        Sourabh = 'Sourabh'
        Sukhmeet = 'Sukhmeet'
        Vishnu = 'Vishnu'
        Sumit = 'Sumit' 
        Other = 'Other'
    
    issue_category = models.CharField(max_length=20, choices=issue_category.choices, default=issue_category.Other)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    issue = models.TextField()
    issue_status = models.CharField(max_length=20, choices=issue_status.choices, default=issue_status.Pending)
    issue_date = models.DateTimeField(auto_now_add=True)
    issue_resolved = models.TextField(blank=True, null=True)
    issue_assigned = models.CharField(max_length=20, choices=AssignedTo.choices, default=AssignedTo.Other)
    screenshot = models.ImageField(upload_to=get_image_name, blank=True, null=True)