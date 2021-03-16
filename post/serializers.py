from django.http import request
from rest_framework import serializers
from .models import post,Comment
from django.shortcuts import render, get_object_or_404
#from profiles.serializers import UserList
from django.utils.timesince import timesince
from rest_framework.validators import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
import datetime


class Postlist(serializers.ModelSerializer):
    update = serializers.HyperlinkedIdentityField(view_name='posts:post-update',lookup_field='pk')
    delete = serializers.HyperlinkedIdentityField(view_name='posts:post-delete',lookup_field='pk')
    details = serializers.HyperlinkedIdentityField(view_name='posts:post-details',lookup_field='pk')
    like = serializers.HyperlinkedIdentityField(view_name='posts:post-like',lookup_field='pk')
    user = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    contents = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField(read_only=True)
    created = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    class Meta:
        model = post
        fields = ['id','user','contents','details','image','total_comments','total_likes','comments','like','users','update','delete','created']

    def get_users(self,obj):
        return f"http://{get_current_site(request)}{obj.author.get_absolute_url()}"
 
    def get_contents(self,obj):
        return obj.contents()

    def get_user(self,obj):
        return str(obj.author)

    def get_total_likes(self,obj):
        return obj.get_total_likes()

    def get_created(self,obj):
        return obj.created_on.strftime("%b-%d-%Y %I:%M %p")

    def get_total_comments(self, obj):
        qs = Comment.objects.filter(post=obj,reply=None).count()
        return qs
    
    def get_comments(self, obj):
        qs = Comment.objects.filter(post=obj,reply=None)
        #print(obj)
        serializer = CommentDetails(qs, many=True)
        return serializer.data


class PostCreate(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    class Meta:
        model = post
        fields = ['content', 'image','created']

    # def get_created(self,obj):
    #     return timesince(obj.created_on) + " ago"

    def get_created(self,obj):
        return obj.created_on.strftime("%b-%d-%Y %I:%M %p")

    def validate(self,data):
        content=data['content']
        image=data['image']
        if not content and not image:
            raise ValidationError("Please fill atleast one post field")
        return data


class PostUpdateDelete(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    class Meta:
        model = post
        fields = ['author','content', 'image','likes','created']
        read_only_fields = ['author']

        def get_user(self,obj):
            return str(obj.author)

    def get_likes(self,obj):
        return obj.get_total_likes()

    def get_created(self,obj):
        return obj.created_on.strftime("%b-%d-%Y %I:%M %p")

class PostDetails(serializers.ModelSerializer):
    update = serializers.HyperlinkedIdentityField(view_name='posts:post-update',lookup_field='pk')
    delete = serializers.HyperlinkedIdentityField(view_name='posts:post-delete',lookup_field='pk')
    like = serializers.HyperlinkedIdentityField(view_name='posts:post-like',lookup_field='pk')
    user = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = post
        fields = ['id','user','content', 'image','likes','total_comments','comments','like','update','delete','created']

    def get_user(self,obj):
        return str(obj.author)

    def get_likes(self,obj):
        return obj.get_total_likes()

    def get_created(self,obj):
        return obj.created_on.strftime("%b-%d-%Y %I:%M %p")

    def get_total_comments(self, obj):
        qs = Comment.objects.filter(post=obj,reply=None).count()
        return qs
    
    def get_comments(self, obj):
        qs = Comment.objects.filter(post=obj,reply=None)
        #print(qs)
        serializer = CommentDetails(qs, many=True)
        return serializer.data
        
        
class CommentList(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='posts:comment-details')
    reply = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id','user','post','comment','reply','replies','url','created']

    def get_user(self,obj):
        return str(obj.author)

    def get_created(self,obj):
        return obj.created_on.strftime("%b-%d-%Y %I:%M %p")

    def get_reply(self,obj):
        return obj.replys().count()
    
    def get_replies(self,obj):
        return Commentchild(obj.replys(),many=True).data
 
 
class Commentchild(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id','user','comment','created']

    def get_user(self,obj):
        return str(obj.author)

    def get_created(self,obj):
        return obj.created_on.strftime("%b-%d-%Y %I:%M %p")

class CommentCreateSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id','comment','created']

    def get_created(self,obj):
        return obj.created_on.strftime("%b-%d-%Y %I:%M %p")

class CommentDetails(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    replies=serializers.SerializerMethodField()
    reply = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id','user','post','comment','reply','replies','created']
        read_only_fields=['post']  

    def get_user(self,obj):
        return str(obj.author)

    def get_created(self,obj):
        return obj.created_on.strftime("%b-%d-%Y %I:%M %p")

    def get_replies(self,obj):
        return Commentchild(obj.replys(),many=True).data
       
    def get_reply(self,obj):
        return obj.replys().count()

