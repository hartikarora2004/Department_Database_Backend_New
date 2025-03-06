from django.db import models

class ApproveRequest(models.Model):
    applicant_name = models.CharField(max_length=255)
    instructor_id = models.IntegerField(default=0)
    achievement_id = models.IntegerField(default=0)  # Or use some meaningful default value
    request_date = models.DateTimeField(auto_now_add=True)  # This will store the date request was made
