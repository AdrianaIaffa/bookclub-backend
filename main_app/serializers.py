from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import BookClub, Comment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'name', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class BookClubSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BookClub
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True},
            'members': {'required': False},
        }

class UserRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password', 'id']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
