from django.db import models
from usercustom.models import CustomUser
from django.core.exceptions import ValidationError

# Create your models here.

def validate_staff(value):
    if isinstance(value, int):
        try:
            value = CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise ValidationError(f'User with id {value} does not exist')
    elif value.is_activated == False:
        raise ValidationError(f'{value.first_name} is not activated')
    if value.groups.filter(name='Staff').exists():
        return value
    else:
        raise ValidationError(f'{value.first_name} is not a Staff')

    
class staffDetails(models.Model):
    class staff_type(models.TextChoices):
        Technical_Staff = 'Technical Staff'
        Administrative_Staff = 'Administrative Staff' 
    staff = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='staff_details', validators=[validate_staff])
    type = models.CharField(max_length=20, choices=staff_type.choices, default=staff_type.Technical_Staff)
    sta_id = models.CharField(max_length=10, default='')
    

    def __str__(self):
        return self.staff.username
    