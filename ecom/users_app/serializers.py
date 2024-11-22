from rest_framework import serializers
from users_app.models import AppUser, Profile
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = ('id', 'email')
        read_only_fields = ('created_at', 'updated_at')


class CreateuserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AppUser
        fields = ('id', 'email', 'password')
        read_only_fields = ('created_at', 'updated_at')
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
        fields = ('id', 'email', 'password',)

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


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = (
            'user', 'profile_picture', 'first_name', 'last_name', 'phone', 
            'date_of_birth', 'address_line1', 'bio', 'academic_background',
        )  
        read_only_fields = ('user', 'email', 'created_at', 'updated_at')


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False, write_only=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False, write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError("Current Password is Incorrect!")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data