from basemodel.models import BaseModel
from usercustom.models import CustomUser
from batch.models import Batch
from department.models import Department
from achievements.models import Achievement
from events.models import Event
from visits.models import Visit
from project.models import Project
from publications.models import Publication
from django.db import models
# Create your models here.

class DinfoMeetingFile(models.Model):
    batches = models.ManyToManyField(Batch, related_name='%(class)s_batches', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='%(class)s_department')
    faculty_achievements = models.ManyToManyField(Achievement, related_name='%(class)s_faculty_achievements', blank=True, null=True)
    student_achievements = models.ManyToManyField(Achievement, related_name='%(class)s_student_achievements', blank=True, null=True)
    events = models.ManyToManyField(Event, related_name='%(class)s_events', blank=True, null=True)
    faculty_visits = models.ManyToManyField(Visit, related_name='%(class)s_faculty_visits',blank=True, null=True)
    student_visits = models.ManyToManyField(Visit, related_name='%(class)s_student_visits',blank=True, null=True)
    publications = models.ManyToManyField(Publication, related_name='%(class)s_publications',blank=True, null=True)
    projects = models.ManyToManyField(Project, related_name='%(class)s_projects',blank=True, null=True)
    year = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

class BogMeetingFile(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='%(class)s_department')
    year = models.IntegerField(null=True, blank=True)
    faculty_achievements = models.ManyToManyField(Achievement, related_name='%(class)s_faculty_achievements', blank=True, null=True)
    student_achievements = models.ManyToManyField(Achievement, related_name='%(class)s_student_achievements', blank=True, null=True)
    events = models.ManyToManyField(Event, related_name='%(class)s_events', blank=True, null=True)
    visits = models.ManyToManyField(Visit, related_name='%(class)s_visits',blank=True, null=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name