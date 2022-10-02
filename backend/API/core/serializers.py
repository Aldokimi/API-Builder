from .models import User, Project
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'is_superuser',
            'username',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'last_login',
            'first_name',
            'last_name',
            'bio',
            'date_of_birth',
            'profile_picture',
            'groups',
            'user_permissions',
        ]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'date_created',
            'last_updated',
            'endpoint_name',
            'private',
            'owner',
        ]