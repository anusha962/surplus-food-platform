from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, label='Confirm password')

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password2',
                   'role', 'phone_number', 'latitude', 'longitude')

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({'password2': "Passwords don't match."})
        return attrs

    def validate_role(self, value):
        if value == CustomUser.Role.ADMIN:
            raise serializers.ValidationError("Can't self-register as admin.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'phone_number',
                   'latitude', 'longitude', 'is_verified', 'date_joined')
        read_only_fields = ('id', 'role', 'is_verified', 'date_joined')