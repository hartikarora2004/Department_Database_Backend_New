from rest_framework import serializers
from .models import StudentProject
from basemodel.serializers import *
from usercustom.models import CustomUser
from usercustom.serializers import UserSerializer

StudentProject_fields = [
                  'title',
                  'description',
                  'start_date',
                  'end_date',
                  'members',
                  'Members',
                  'mentor',
                  'Mentor'
                ]

StudentProject_kwargs = {
            'members': {'write_only': True, 'required': True},
            'mentor': {'write_only': True, 'required': True}
        }

class StudentProjectSerializer(BaseSerializer):
    Members = UserSerializer(many=True,read_only=True, source='members.all')
    Mentor = UserSerializer(read_only=True, source='mentor')
    model = StudentProject

    def get_users_str(self):
        return ",".join([str(user) for user in self.validated_data['members']])

    def generate_tags(self):
        arr = [False,False,False,False,False]
        tags = ['faculty', 'undergraduate', 'postgraduate', 'phd', 'staff']
        output = ''
        dict_map = {}
        dict_map['fc'] = 0
        dict_map['ug'] = 1
        dict_map['pg'] = 2
        dict_map['phd'] = 3
        dict_map['st'] = 4
        for user in self.validated_data['members']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]
    class Meta:
        model = StudentProject
        fields = model_basic_fields + StudentProject_fields
        extra_kwargs = {**model_base_kwargs , **StudentProject_kwargs}
    
    def validate(self, data):
        errors = {}
        for value in data['members']:
            if not value.is_activated:
                errors.setdefault('members', []).append("User is not activated")
            if not value.groups.filter(name='Student').exists():
                errors.setdefault('members', []).append(f"User {value.username} with id {value.id} is not a student")
        if errors:
            raise serializers.ValidationError(errors)
        return data


class StudentProjectDraftSerializer(BaseDraftSerializer):
    Members = UserSerializer(many=True,read_only=True, source='members.all')
    Mentor = UserSerializer(read_only=True, source='mentor')
    model = StudentProject

    def get_users_str(self):
        return ",".join([str(user) for user in self.validated_data['members']])
    
    def generate_tags(self):
        arr = [False,False,False,False,False]
        tags = ['faculty', 'undergraduate', 'postgraduate', 'phd', 'staff']
        output = ''
        dict_map = {}
        dict_map['fc'] = 0
        dict_map['ug'] = 1
        dict_map['pg'] = 2
        dict_map['phd'] = 3
        dict_map['st'] = 4
        for user in self.validated_data['members']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]
    
    class Meta:
        model = StudentProject
        fields = model_basic_fields + StudentProject_fields
        extra_kwargs = {**model_base_kwargs , **StudentProject_kwargs}

    def validate(self, data):
        errors = {}
        for value in data['members']:
            if not value.is_activated:
                errors.setdefault('members', []).append("User is not activated")
            if not value.groups.filter(name='Student').exists():
                errors.setdefault('members', []).append(f"User {value.username} with id {value.id} is not a student")
        if errors:
            raise serializers.ValidationError(errors)
        return data
    

class StudentProjectDraftUpdateSerializer(BaseDraftUpdateSerializer):
    Members = UserSerializer(many=True,read_only=True, source='members.all')
    Mentor = UserSerializer(read_only=True, source='mentor')
    model = StudentProject

    def get_users_str(self):
        return ",".join([str(user) for user in self.validated_data['members']])

    def generate_tags(self):
        arr = [False,False,False,False,False]
        tags = ['faculty', 'undergraduate', 'postgraduate', 'phd', 'staff']
        output = ''
        dict_map = {}
        dict_map['fc'] = 0
        dict_map['ug'] = 1
        dict_map['pg'] = 2
        dict_map['phd'] = 3
        dict_map['st'] = 4
        for user in self.validated_data['members']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]

    class Meta:
        model = StudentProject
        fields = model_basic_fields + StudentProject_fields
        extra_kwargs = {**model_base_kwargs , **StudentProject_kwargs}

    def validate(self, data):
        errors = {}
        for value in data['members']:
            if not value.is_activated:
                errors.setdefault('members', []).append("User is not activated")
            if not value.groups.filter(name='Student').exists():
                errors.setdefault('members', []).append(f"User {value.username} with id {value.id} is not a student")
        if errors:
            raise serializers.ValidationError(errors)
        return data
    

StudentProject_list_fields = [
                  'id',
                  'users',
                  'department',
                  'title',
                  'description',
                  'start_date',
                  'end_date',
                  'members',
                  'mentor',
                  'tags',
                    'status',
                ]

class StudentProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProject
        fields = StudentProject_list_fields