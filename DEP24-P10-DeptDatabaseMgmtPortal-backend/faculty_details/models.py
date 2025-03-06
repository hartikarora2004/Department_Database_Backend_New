from django.db import models
from usercustom.models import CustomUser
from django.core.exceptions import ValidationError

# Create your models here.

def validate_faculty(value):
    if isinstance(value, int):
        try:
            value = CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise ValidationError(f'User with id {value} does not exist')
    elif value.is_activated == False:
        raise ValidationError(f'{value.first_name} is not activated')
    # if value.groups.filter(name='fc').exists():
    #     return value
    # else:
    #     raise ValidationError(f'{value.first_name} is not a Faculty')
    if value.user_type=='fc':
        print("faculty found: ",value)
        return value
    else:
        raise ValidationError(f'{value.first_name} is not a Faculty')


class facultyDetails(models.Model):
    designations = [
        ('Assistant Professor', 'Assistant Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Professor', 'Professor'),
    ]
    faculty = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='faculty_details', validators=[validate_faculty])
    designation = models.CharField(max_length=30, choices=designations, default='Assistant Professor')
    fields_of_interest = models.TextField(null=True, blank=True)
    phd_instuition = models.TextField(null=True, blank=True)
    fac_id = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.faculty.username
    