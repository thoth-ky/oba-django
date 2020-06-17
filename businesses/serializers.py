from rest_framework import serializers
from businesses.models import Business
from user.serializers import UserSerializer

class BusinessSerializer(serializers.ModelSerializer):
  owner = UserSerializer(read_only=True)
  class Meta:
    model = Business
    fields = '__all__'
    depth=1
  
  def create(self, validated_data):
    owner = self.context['request'].user
    return Business.objects.create(owner=owner, **validated_data)