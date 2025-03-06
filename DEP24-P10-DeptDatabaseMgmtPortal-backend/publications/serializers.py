from rest_framework import serializers
from .models import Publication, PublicationEditHistory
from basemodel.serializers import *
from usercustom.serializers import *

Publication_fields = [
                  'title',
                  'description',
                  'link',
                  'publication_type',
                  'publication_status',
                  'identifier_type',
                  'identifier',
                  'Authors',
                  'authors',
                  'authors_text',
                  'published_date',
                  'accepted_date',
                  'field_tags',
                ]

Publication_kwargs = {
            'authors': {'write_only': True, 'required': True}
        }

class PublicationSerializer(BaseSerializer):
    Authors = UserSerializer(many=True,read_only=True, source='authors.all')
    model = Publication

    def get_users_str(self):
        return self.validated_data['authors_text']
    
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
        for user in self.validated_data['authors']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]
    class Meta:
        model = Publication
        fields = model_basic_fields + Publication_fields
        extra_kwargs = {**model_base_kwargs , **Publication_kwargs}

    def validate(self,data):
        errors = {}
        for value in data['authors']:
            if value.is_activated == False:
                errors.setdefault('authors', []).append("User is not activated")
            if not value.groups.filter(name='Faculty').exists():
                if not value.groups.filter(name='Student').exists():
                    errors.setdefault('authors', []).append(f"User {value.username} with id {value.id} is not a faculty or student")
            if errors:
                raise serializers.ValidationError(errors)
        return data

class PublicationDraftSerializer(BaseDraftSerializer):
    Authors = UserSerializer(many=True,read_only=True, source='authors.all')
    model = Publication

    def get_users_str(self):
        return self.validated_data['authors_text']

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
        for user in self.validated_data['authors']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]
    class Meta:
        model = Publication
        fields = model_basic_fields + Publication_fields
        extra_kwargs = {**model_base_kwargs , **Publication_kwargs}

    def validate(self,data):
        errors = {}
        for value in data['authors']:
            if value.is_activated == False:
                errors.setdefault('authors', []).append("User is not activated")
            if not value.groups.filter(name='Faculty').exists():
                if not value.groups.filter(name='Student').exists():
                    errors.setdefault('authors', []).append(f"User {value.username} with id {value.id} is not a faculty or student")
            if errors:
                raise serializers.ValidationError(errors)
        return data


class PublicationDraftUpdateSerializer(BaseDraftUpdateSerializer):
    Authors = UserSerializer(many=True,read_only=True, source='authors.all')
    model = Publication

    def get_users_str(self):
        return self.validated_data['authors_text']

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
        for user in self.validated_data['authors']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]
    class Meta:
        model = Publication
        fields = model_basic_fields + Publication_fields
        extra_kwargs = {**model_base_kwargs , **Publication_kwargs}
    
    def validate(self,data):
        errors = {}
        for value in data['authors']:
            if value.is_activated == False:
                errors.setdefault('authors', []).append("User is not activated")
            if not value.groups.filter(name='Faculty').exists():
                if not value.groups.filter(name='Student').exists():
                    errors.setdefault('authors', []).append(f"User {value.username} with id {value.id} is not a faculty or student")
            if errors:
                raise serializers.ValidationError(errors)
        return data
    

Publication_list_fields = [
                  'id',
                  'department',
                  'users',
                  'title',
                  'description',
                  'link',
                  'publication_type',
                  'publication_status',
                  'identifier_type',
                  'identifier',
                  'authors',
                  'authors_text',
                  'published_date',
                  'accepted_date',
                  'tags',
                  'created_by',
                  'field_tags',
                ]

class PublicationListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.first_name', read_only=True)
    
    class Meta:
        model = Publication
        fields = Publication_list_fields

class PublicationEditHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationEditHistory
        fields = '__all__'