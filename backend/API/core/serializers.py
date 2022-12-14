from .models import User, Project
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'date_of_birth', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(username = self.validated_data['username'], email=self.validated_data['email'], date_of_birth=self.validated_data['date_of_birth'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'username',
            'email',
            'is_active',
            'is_admin',
            'linkedin_token',
            'date_joined',
            'last_login',
            'first_name',
            'last_name',
            'bio',
            'date_of_birth',
            'profile_picture',
        ]
        extra_kwargs = {
            'password': {'write_only':True}
        }


class UpdateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=False)
    email = serializers.CharField(max_length=100, required=False)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'is_active',
            'is_admin',
            'linkedin_token',
            'date_joined',
            'last_login',
            'first_name',
            'last_name',
            'bio',
            'date_of_birth',
            'profile_picture',
        ]

class CreateProjectSerializer(serializers.ModelSerializer):
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
            'file_name',
            'file_content',
            'file_type',
        ]

class UpdateProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=False)
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'date_created',
            'last_updated',
            'endpoint_name',
            'private',
            'file_name',
            'file_content',
            'file_type',
        ]
