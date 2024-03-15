from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import TokenError, RefreshToken
from django.contrib.auth import  authenticate
from django.contrib.auth.password_validation import validate_password
from accounts.methodes import *


##### sign up serializer #####
class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['phonenumber','email', 'username', 'password','password2']
        extra_kwargs = {
            'password':{'write_only':True,}
        }
    def validate(self, validated_data):
        password = validated_data['password']
        password2 = validated_data.pop('password2')
        validate_password(password)
        validate_password(password2)
        if password != password2:
            raise serializers.ValidationError("passwords don't match")

        return validated_data

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    


##### login serializer #####
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise serializers.ValidationError("Incorrect Credentials")
            if not user.is_active:
                raise serializers.ValidationError({'message_error':'this account is not active'})
            if not user.is_verified:
                raise serializers.ValidationError({'message_error':'this account is not verified'})
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        data['user'] = user
        return data
    
##### logout serializer #####
class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


##### reset password serializer #####
class ResetPasswordSerializer(serializers.Serializer):
    newpassword = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['newpassword']:
            raise serializers.ValidationError({'message_error':'Passwords do not match.'})
        validate_password(attrs['newpassword'])
        return attrs

    def update(self, instance, validated_data):
        pk = self.context.get('pk')
        instance = CustomUser.objects.get(pk=pk)
        instance.set_password(validated_data['newpassword'])
        instance.save()
        code = CodeVerification.objects.filter(user=instance).first()
        code.delete()
        return instance


# Handel Seriailzer For List Information User
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'image']




class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'