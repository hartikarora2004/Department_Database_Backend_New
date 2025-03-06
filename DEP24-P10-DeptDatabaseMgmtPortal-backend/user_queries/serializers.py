from rest_framework.serializers import ModelSerializer
from user_queries.models import QueryModel
from rest_framework import serializers


class QuerySerializer(ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = QueryModel
        fields = ['issue_category', 'issue', 'screenshot','user_name', 'user']

