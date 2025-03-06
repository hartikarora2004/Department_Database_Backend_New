from django.db import models
from usercustom.models import CustomUser
from django.core.exceptions import ValidationError
# Create your models here.

def validate_faculty_advisor(value):
    if isinstance(value, int):
        try:
            value = CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise ValidationError(f'User with id {value} does not exist')
    elif value.is_activated == False:
        raise ValidationError(f'{value.first_name} is not activated')
    if value.groups.filter(name='Faculty').exists():
        return value
    else:
        raise ValidationError(f'{value.first_name} is not a Faculty Advisor')

def validate_student(value):
    if isinstance(value, int):
        try:
            value = CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise ValidationError(f'User with id {value} does not exist')
    elif value.is_activated == False:
        raise ValidationError(f'{value.first_name} is not activated')
    if value.groups.filter(name='Student').exists():
        return value
    else:
        raise ValidationError(f'{value.first_name} is not a Student')


class studentDetails(models.Model):

    class degrees(models.TextChoices):
        BTECH = 'B.Tech'
        MTECH = 'M.Tech'
        PHD = 'Ph.D'
        MSC = 'M.Sc'


    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='student_details', validators=[validate_student])
    faculty_advisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_faculty_advisor', validators=[validate_faculty_advisor])
    degree = models.CharField(max_length=10, choices=degrees.choices, default=degrees.BTECH)
    batch = models.ForeignKey('batch.Batch', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_batch')
    entry_no = models.CharField(max_length=20, default='')

    def __str__(self):
        return str(self.student)
