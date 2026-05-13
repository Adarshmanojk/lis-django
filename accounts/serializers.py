"""
Serializers for the accounts app.
Handles user creation (with hashed password), profile updates, and access rules.
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, UserAccessMaster


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True, default='')
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'email', 'password',
            'employee_id', 'full_name', 'role',
            'designation', 'department', 'phone', 'status',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({'password': 'Password is required when creating a user.'})
        username = validated_data.pop('username')
        email = (validated_data.pop('email', '') or '').strip()
        auth_user = User.objects.create_user(username=username, email=email, password=password)
        return UserProfile.objects.create(user=auth_user, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        username = validated_data.pop('username', None)
        email = validated_data.pop('email', None)
        if password:
            instance.user.set_password(password)
        if username is not None:
            instance.user.username = username
        if email is not None:
            instance.user.email = email
        instance.user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccessMaster
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
