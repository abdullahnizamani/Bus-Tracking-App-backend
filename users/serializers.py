from rest_framework import serializers
from .models import User
from knox import views as knox_views
from django.contrib.auth import authenticate
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

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
    