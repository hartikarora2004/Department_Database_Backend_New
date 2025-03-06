from rest_framework import serializers
from usercustom.models import CustomUser
from department.serializers import DepartmentSerializer

model_basic_fields = [
    'id',
    'updated_by',
    'created_by',
    'deleted_by',
    'department',
    'Department',
    'object_type',
    'draft_id',
    'is_deleted',
    'users',
    'tags',
]

model_base_kwargs = {
    'id': {'read_only': True, 'required': False},
    'object_type': {'read_only': True, 'required': False},
    'draft_id': {'read_only': True, 'required': False},
    'is_deleted': {'read_only': True, 'required': False},
    'users': {'read_only': True, 'required': False},
    'tags': {'read_only': True, 'required': False},
}


class BaseSerializer(serializers.ModelSerializer): 
    Department = DepartmentSerializer(many=True,read_only=True, source='department.all')
    created_by = serializers.CharField(source='creator.username', read_only=True)
    updated_by = serializers.CharField(source='created_by.username', read_only=True)
    deleted_by = serializers.CharField(source='deleted_by.username', read_only=True)

    def get_users_str(self):
        return ""

    def generate_tags(self):
        return ""
    
    def create(self,data):
        data['draft_id'] = None
        data['is_draft'] = False
        data['is_deleted'] = False
        data['is_approved'] = True
        data['created_by'] = self.context['request'].user
        data['creator'] = self.context['request'].user
        data['users'] = self.get_users_str()
        data['tags'] = self.generate_tags()
        obj = super().create(data)
        return obj
    
    def update(self,instance,data):
        instance = super().update(instance,data)
        instance.users = self.get_users_str()
        instance.tags = self.generate_tags()
        return instance

    def delete(self):
        instance = self.instance
        instance.soft_delete(self.context['request'].user)
        return instance

    def restore(self,instance):
        instance.restore()
        return instance

class BaseDraftSerializer(serializers.ModelSerializer):
    Department = DepartmentSerializer(many=True,read_only=True, source='department.all')
    created_by = serializers.CharField(source='creator.username', read_only=True)
    updated_by = serializers.CharField(source='created_by.username', read_only=True)
    deleted_by = serializers.CharField(source='deleted_by.username', read_only=True)

    def get_users_str(self):
        return ""
    
    def generate_tags(self):
        return ""

    def create(self,data):
        data['draft_id'] = None
        data['is_draft'] = True
        data['is_approved'] = False
        data['created_by'] = self.context['request'].user
        data['creator'] = self.context['request'].user
        data['is_deleted'] = False
        data['users'] = self.get_users_str()
        data['tags'] = self.generate_tags()
        data['object_type'] = 'DR'
        obj = super().create(data)
        return obj
    
    def update(self,instance,data):
        instance.delete_object_drafts(self.model)
        dict = instance.__dict__.copy()
        del dict['_state'] 
        dict['draft_id'] = dict['id']
        del dict['id'] 
        dict['is_draft'] = True
        dict['is_approved'] = False
        dict['users'] = self.get_users_str()
        dict['tags'] = self.generate_tags()
        dict['object_type'] = 'DR'
        x = self.model.drafts.create(**dict)
        x = super().update(x,data)
        x.object_type = self.model.object_status.DRAFT
        x.created_by = self.context['request'].user
        x.save()
        return x

class BaseDraftUpdateSerializer(serializers.ModelSerializer):
    Department = DepartmentSerializer(many=True,read_only=True, source='department.all')
    created_by = serializers.CharField(source='creator.username', read_only=True)
    updated_by = serializers.CharField(source='created_by.username', read_only=True)
    deleted_by = serializers.CharField(source='deleted_by.username', read_only=True)

    def get_users_str(self):
        return ""
    
    def generate_tags(self):
        return ""
    
    def update(self,instance,data):
        print('update prev start')
        obj = super().update(instance,data)
        print('update prev end')
        obj.is_draft = True
        obj.is_approved = False
        obj.created_by = self.context['request'].user
        obj.users = self.get_users_str()
        obj.tags = self.generate_tags()
        obj.save()
        return obj