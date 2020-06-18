from rest_framework import serializers
from django.contrib.auth import authenticate
from user.models import User
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password', 'last_login', 'is_superuser', 'is_active')
    read_only_fields = ('last_login', 'is_superuser', 'is_active')
    extra_kwargs = {
        'password': {'write_only': True}
    }
  
  def create(self, validated_data):
    user = User(**validated_data)
    user.set_password(validated_data["password"])
    user.save()
    return user
  


class AuthSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()

  def validate(self, attrs):
    username = attrs.get('username')
    password = attrs.get('password')

    if username and password:
      user = authenticate(username=username, password=password)

      if user:
        if not user.is_active:
          msg = 'User account is disabled.'
          raise serializers.ValidationError(msg, code='authorization')
      else:
        msg = 'Unable to log in with provided credentials.'
        raise serializers.ValidationError(msg, code='authorization')

    else:
      msg = 'Must include "username" and "password"'
      raise serializers.ValidationError(msg, code='authorization')
    attrs['user'] = user
    return attrs
