from rest_framework import serializers
from .models import *

class LinkerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkerUser
        fields = ('id',
                  'password','last_login','is_superuser','username','first_name',
                  'last_name','email','is_staff','is_active','date_joined','quote',
                  'birth_date',)
        read_only_fields = ('id','last_login','is_superuser','is_staff',
                            'is_active','date_joined',)
        
class LinkerUserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkerUserPhoto
        fields = ('id', 'photo')

class SubscriptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ('created_at',)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('follower', 'following'),
                message='Subscription already exists for this follower and following.'
            )
        ]
    def validate(self, data):
        follower = data['follower']
        following = data['following']

        if follower == following:
            raise serializers.ValidationError(
                "Follower and following cannot be the same.",
            )
        return data