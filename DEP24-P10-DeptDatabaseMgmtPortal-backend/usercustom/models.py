from django.db import models
from .manager import UserManager,UserManagerfiltered
from django.contrib.auth.models import AbstractUser


def profile_upload_path(instance, filename):
    if filename == None or filename == '':
        return 'upload/profile.png'
    extension = filename.split('.')[-1]
    return f'upload/profile_images/{instance.id}.{extension}'

def cover_upload_path(instance, filename):
    if filename == None or filename == '':
        return None
    extension = filename.split('.')[-1]
    return f'upload/cover_images/{instance.id}.{extension}'

class CustomUser(AbstractUser):
    class UserTypes(models.TextChoices):
        faculty = 'fc', 'Faculty'
        ug_student = 'ug', 'ug_student'
        pg_student = 'pg', 'pg_student'
        phd_student = 'phd', 'phd_student'
        staff = 'st', 'staff'
        super_admin = 'sa', 'super_admin'

    user_type = models.CharField(max_length=5, choices=UserTypes.choices, default= UserTypes.ug_student)
    email = models.EmailField(unique=True)
    doctorate_degree = models.BooleanField(default=False)
    username = models.TextField(null=True, blank = True)
    phone_no = models.TextField(null=True, blank = True)
    is_activated = models.BooleanField(default=False)
    department = models.ForeignKey('department.Department', on_delete=models.CASCADE, null=True, blank=True)
    get_email_notification = models.BooleanField(default=True)
    get_email_broadcast_notification = models.BooleanField(default=True)
    get_otp_email = models.BooleanField(default=True)
    is_current = models.BooleanField(default=True)
    year = models.IntegerField(default=2020)
    profile_image = models.ImageField(upload_to= profile_upload_path, default='upload/profile.png', null=True, blank=True)
    cover_image = models.ImageField(upload_to= cover_upload_path, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    

    #this is the unique identifier for the user
    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        if self.doctorate_degree:
            return f'Dr.{self.first_name} {self.last_name}'
        return f'{self.first_name} {self.last_name}'
    def pub_name(self):
        temp = ''
        for i in self.first_name.split(' '):
            temp += i[0] + '.'
        temp = f'{temp} {self.last_name}'
        if self.doctorate_degree:
            return f'Dr.{temp}'
        return temp
    objectsall = UserManager()
    objects = UserManagerfiltered()
