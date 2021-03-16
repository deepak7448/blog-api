from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profiles

class UserList(serializers.ModelSerializer):
    update = serializers.HyperlinkedIdentityField(view_name='profile:profile-update', lookup_field='username',)
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields=['username','first_name','last_name','update']

    def get_first_name(self,obj):
        if obj.first_name:
            return obj.first_name
        else:
            return None
        
    def get_last_name(self,obj):
        if obj.last_name:
            return obj.last_name
        else:
            return None

class ProfilesList(serializers.ModelSerializer):
    bio = serializers.SerializerMethodField()
    facebook_url = serializers.SerializerMethodField()
    instagram_url = serializers.SerializerMethodField()
    Total_post = serializers.SerializerMethodField()
    user=UserList()
    class Meta:
        model = Profiles
        fields = ['user','profile_pic','bio', 'country', 'facebook_url','instagram_url','date_of_birth','Total_post']

    def get_bio(self,obj):
        if obj.bio:
            return obj.bio
        else:
            return None
        
    def get_facebook_url(self,obj):
        if obj.facebook_url:
            return obj.facebook_url
        else:
            return None

    def get_instagram_url(self,obj):
        if obj.instagram_url:
            return obj.instagram_url
        else:
            return None

    def get_Total_post(self,obj):
        return obj.all_post()

class ProfilesUpdate(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ['profile_pic','bio', 'country', 'facebook_url','instagram_url','date_of_birth']

class UpdateUserSerializer(serializers.ModelSerializer):
    profile = ProfilesUpdate()
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'profile']


    def update(self,instance,validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        profile.profile_pic = profile_data.get('profile_pic',profile.profile_pic)
        profile.bio = profile_data.get('bio',profile.bio)
        profile.country = profile_data.get('country',profile.country)
        profile.facebook_url = profile_data.get('facebook_url',profile.facebook_url)
        profile.instagram_url = profile_data.get('instagram_url',profile.instagram_url)
        profile.date_of_birth = profile_data.get('date_of_birth',profile.date_of_birth)
        # profile.profile_pic = profile_data.get('profile_pic',profile.profile_pic)
        # profile.has_support_contract = profile_data.get('has_support_contract',profile.has_support_contract)
        profile.save()
        return instance
