from rest_framework import serializers
from .models import User, Driver, Student
from knox import views as knox_views
from django.contrib.auth import authenticate


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar']


class DriverSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    class Meta:
        model = Driver
        fields = ['employee_id', 'license_id', 'user']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'bus']

class UserSerializer(serializers.ModelSerializer):
    driver = DriverSerializer(read_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'avatar','phone', 'driver', 'student')



class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(style={'input_type': 'username'}, trim_whitespace=False)
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
    def validate(self, attrs):
        user = attrs.get('user')
        password = attrs.get('password')

        if not user or not password:
            raise serializers.ValidationError('Please enter both fields')
        if User.objects.filter(username=user).exists():
            user = authenticate(request=self.context.get('request'), username=user, password=password)
            if not user:
                raise serializers.ValidationError('Wrong credentials')
            
            attrs['user']=user
            return attrs
    