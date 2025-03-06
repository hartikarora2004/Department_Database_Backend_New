from django.db import models
from basemodel.models import BaseModel
from usercustom.models import CustomUser
from django.core.exceptions import ValidationError

# Create your models here.

def validate_head(value):
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
        raise ValidationError(f'{value.first_name} is not a Head')

class ResearchLab(BaseModel):
    lab_types = [
        ('UG Lab', 'UG Lab'),
        ('PG Lab', 'PG Lab'),
        ('Research Lab', 'Research Lab'),
    ]

    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    Head = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_head', validators=[validate_head])
    address  = models.TextField(null=True, blank=True)
    lab_type = models.CharField(max_length=20, choices=lab_types, default=lab_types[0][0])
    equipments = models.TextField(default="")
    

    def __str__(self):
        return self.name

    class Meta:
        constraints = [models.CheckConstraint(check=~(models.Q(is_draft=True) & models.Q(is_approved=True)), name='research lab draft cannot be approved'),
                       models.UniqueConstraint(fields=['draft_id', 'is_approved', 'is_deleted'], condition=models.Q(is_approved=False) & models.Q(is_deleted = False), name='research lab Only one draft can be made for each object'),
                       models.UniqueConstraint(fields=['code', 'is_approved'], condition= models.Q(is_deleted = False), name="research_lab_code_is_unique"),
                    ]