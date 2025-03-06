from django.db import models
from usercustom.models import CustomUser
from django.core.exceptions import ValidationError
# Create your models here.


def validate_hod(value):

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
        raise ValidationError(f'{value.first_name} is not a Hod')


class Department(models.Model):
    
    name = models.CharField(max_length=50, default='')
    code = models.CharField(max_length=5, unique=True, default='')
    description = models.TextField(null=True, blank=True)
    Hod = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_Hod', validators=[validate_hod])
    programs_offered = models.TextField(default="BTech CSE, MTech CSE, MTech AI")

    def __str__(self):
        return self.code