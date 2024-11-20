from rest_framework import serializers
from users_app.models import AppUser
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = ['id', 'email', 'first_name', 'last_name']


class CreateuserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AppUser
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'required': True}
        }

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        if AppUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("User in this email already exists.")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = AppUser.objects.create_user(password=password, **validated_data)
        return user
        
    

class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = ['id', 'email', 'first_name', 'last_name', 'password']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance     


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Please give both email and password!")
        
        if not AppUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email doesn't Exist, Register yourself first to login!")
        
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Wrong Credentials!")
        
        attrs['user'] = user
        return attrs
    

class EmailCheckSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not AppUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No User is associated to this email!")
        return value


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not AppUser.objects.filter(email=value).exists:
            raise serializers.ValidationError("No User is associated to this email!")
        return value
