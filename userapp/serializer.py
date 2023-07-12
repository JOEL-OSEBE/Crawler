# -*- coding: utf-8 -*-
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, CrawlerModel



class RegisterSerializer(serializers.ModelSerializer):
   
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 
                  'date_of_birth','country','token')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',
                  'token')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_admin(**validated_data)


class RegisterSuperAdminSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User

        fields = ('id', 'username', 'password', 'email', 'token')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_superadmin(**validated_data)


class MyLoginPairSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200, read_only=True)
    username = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(
        max_length=200, write_only=True, required=True)
    token = serializers.CharField(max_length=200, read_only=True)

    def validate(self, data):

        username = data.get('username', None)
        password = data.get('password', None)
        # Raise an exception if an
        # email is not provided.
        if username is None:
            raise serializers.ValidationError(
                'A valid username is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A valid password is required to log in.'
            )

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.')

        return {
            'status': 'success',
            'username': user.username,
            'token': user.token
        }


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)


class UserUpdateSerializer(serializers.Serializer):
    model = User
    """
    Profile update
    """
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    date_of_birth = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200)
    

class UserDeactivateSerializer(serializers.Serializer):
    model = User
    """
    Profile update
    """
    email = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200)
    is_active = serializers.BooleanField(required=True)


class UserActivateSerializer(serializers.Serializer):
    model = User
    email = serializers.CharField(required=True)


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:

        model = User
        fields = '__all__'


class CrawlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlerModel
        fields = ['title','source','text','tokens','date','url']
