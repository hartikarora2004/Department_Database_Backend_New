# import 
from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from otplogin.models import Otpdetails
from django.contrib.auth.models import Group
from student_details.models import studentDetails
from faculty_details.models import facultyDetails
from staff_details.models import staffDetails
from rest_framework import serializers
from publications.models import Publication


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many = True)
    profile_image = serializers.ImageField(required = False)
    cover_image = serializers.ImageField(required = False)

    class Meta:
        model = CustomUser
        fields = ["id",
                  "first_name", 
                  "last_name", 
                  "email",
                  "groups",
                  "username",
                  "get_otp_email",
                  "get_email_broadcast_notification",
                  "get_email_notification",
                  "department",
                  "is_current",
                  "year",
                  "user_type",
                  "doctorate_degree",
                  "profile_image",
                  "cover_image",
                  "is_active",
                  "description"
                ]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


#Serializer to Register User
# class RegisterSerializer(serializers.ModelSerializer):
#   email = serializers.EmailField(
#     required=True,
#     validators=[UniqueValidator(queryset=CustomUser.objects.all())]
#   )
#   password = serializers.CharField(
#     write_only=True, required=True, validators=[validate_password])
#   password2 = serializers.CharField(write_only=True, required=True)
#   group = serializers.CharField(write_only=True, required=True)
#   class Meta:
#     model = CustomUser
#     fields = ('username','password', 'password2',
#          'email', 'first_name', 'last_name','group','get_otp_email','get_email_notification','get_email_broadcast_notification', 'department',"year","user_type","doctorate_degree")



#   def validate(self, attrs):
#     if attrs['password'] != attrs['password2']:
#       raise serializers.ValidationError(
#         {"password": "Password fields didn't match."})
#     return attrs
#   def create(self, validated_data):
#     print(validated_data['email'][-13:])
#     if validated_data['email'][-13:] != '@iitrpr.ac.in':
#       raise serializers.ValidationError(
#         {"email": "Please use IIT Ropar email id."}
#         )
#     user = CustomUser.objects.create(
#       username=validated_data['username'],
#       email=validated_data['email'],
#       first_name=validated_data['first_name'],
#       last_name=validated_data['last_name'],
#       department = validated_data['department'],
#       year = validated_data['year'],
#     )
#     current = Group.objects.get(name = validated_data['group'])
#     user.groups.set([current]) 
#     user.save()
#     otp = Otpdetails.objects.create(user = user)
#     otp.setup(user)
#     otp.save()
#     user.set_password(validated_data['password'])
#     if user.groups.filter(name = 'Student').exists():
#           obj = studentDetails.objects.create(student = user)
#           if self.context['request'].user!=None and self.context['request'].user.groups.filter(name = 'Faculty').exists():
#               obj.faculty_advisor = self.context['request'].user
#               user.department = self.context['request'].user.department
#               user.is_activated = True
#               user.save()
#           obj.save()
#     elif user.groups.filter(name = 'Faculty').exists():
#           obj = facultyDetails.objects.create(faculty = user)
#           obj.save()
#     elif user.groups.filter(name = 'Staff').exists():
#           obj = staffDetails.objects.create(staff = user)
#           obj.save()
#     return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    email = serializers.EmailField()