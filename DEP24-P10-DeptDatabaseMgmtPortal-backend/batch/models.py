from django.db import models

# Create your models here.

class Batch(models.Model):
    name = models.CharField(max_length=50, default='')
    year = models.IntegerField(default=2020)
    department = models.ForeignKey('department.Department', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_department')

    def __str__(self):
        return self.name
        