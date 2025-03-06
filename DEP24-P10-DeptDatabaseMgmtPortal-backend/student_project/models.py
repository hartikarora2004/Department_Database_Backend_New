from django.db import models
from basemodel.models import BaseModel
from usercustom.models import CustomUser
from department.models import Department
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
    if value.groups.filter(name='Faculty').exists():
        return value
    else:
        raise ValidationError(f'{value.first_name} is not a faculty')

class StudentProject(BaseModel):

    class ProjectStatus(models.TextChoices):
        ONGOING = 'ON', "ONGOING"
        COMPLETED = 'CO', "COMPLETED"
        CANCELLED = 'CA', "CANCELLED"

    title = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    members = models.ManyToManyField(CustomUser, related_name='%(class)s_members')
    mentor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_mentor', validators=[validate_faculty])
    status = models.CharField(max_length=2, choices=ProjectStatus.choices, default=ProjectStatus.ONGOING)

    def __str__(self):
        return self.title
    
    class Meta:
        constraints = [models.CheckConstraint(check=~(models.Q(is_draft=True) & models.Q(is_approved=True)), name='student project draft cannot be approved'),
                       models.UniqueConstraint(fields=['draft_id', 'is_approved', 'is_deleted'], condition=models.Q(is_approved=False) & models.Q(is_deleted = False), name='Only one student project draft can be made for each object'),
                    ]