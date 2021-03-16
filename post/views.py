from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User
from .serializers import (PostCreate,
                          Postlist,
                          CommentList,
                          CommentDetails,
                          PostDetails,
                          PostUpdateDelete,
                          CommentCreateSerializer,)
from rest_framework import generics
from rest_framework.generics import( ListAPIView,
                                    CreateAPIView,
                                    RetrieveDestroyAPIView,
                                    RetrieveUpdateAPIView,
                                    RetrieveAPIView)
from rest_framework.mixins import DestroyModelMixin,UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import post,Comment
from profiles.models import Profiles
from .permissions import IsOwnerOrReadOnly

class PostList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = post.objects.all()
    serializer_class = Postlist
    #filter_backends = [DjangoFilterBackend]
    filter_backends = [SearchFilter]
    search_fields = ['author__user__username','content']
    #filterset_fields = ['author']
    permission_classes = [IsAuthenticated]

# class PostList(APIView):
#     serializer_class = PostCreate
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     filter_backends = [SearchFilter]
#     search_fields = ['author__user__username']
  
#     def get(self, request,*args, **kwargs):
#         posts = post.objects.all()
#         serializer_context = {
#             'request': request,
#         }
#         serializer = PostDetails(posts,many=True,context=serializer_context)
#         return Response(serializer.data, status=200)

#     def post(self, request,*args, **kwargs):
       
#         serializer = PostCreate(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=Profiles.objects.get(user=self.request.user))
#             return Response(serializer.data, status=200)
#         else:
#             return Response({"errors": serializer.errors}, status=400)

class PostDetail(RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = post.objects.all()
    serializer_class = PostDetails
    permission_classes = [IsAuthenticated]
    lookup_field='pk'
        

# class PostDetail(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     serializer_class = CommentCreateUpdateSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request,pk,*args, **kwargs):
#         posts = get_object_or_404(post,pk=pk)
#         serializer_context = {
#             'request': request,
#         }
#         serializer = PostDetails(posts,context=serializer_context)
#         return Response(serializer.data, status=200)


#     def post(self, request, id, *args, **kwargs):
#         profile = Profiles.objects.get(user=request.user)
#         posts = get_object_or_404(post, id=id)
#         serializer = CommentCreateUpdateSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(author=profile, post=posts)
#             return Response(serializer.data, status=200)
#         else:
#             return Response({"errors": serializer.errors}, status=400)


class Postcreate(CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = post.objects.all()
    serializer_class = PostCreate
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(author=Profiles.objects.get(user=self.request.user))

class PostUpdate(RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = post.objects.all()
    serializer_class = PostUpdateDelete
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    lookup_field='pk'

    def perform_update(self,serializer):
        serializer.save(author=Profiles.objects.get(user=self.request.user))

class PostDelete(DestroyModelMixin,RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = post.objects.all()
    # posts = get_object_or_404(post, id=id)
    serializer_class = PostUpdateDelete
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    #lookup_field='pk'

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class PostLike(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
 
    def get(self, request,pk=None,format=None):
        obj = get_object_or_404(post,pk=pk)
        urls = obj.get_like_url()
        user = self.request.user
        updated = False
        liked = False
        if user not in obj.liked.all():
            liked = True
            obj.liked.add(user)
        else:
            liked = False
            obj.liked.remove(user) 
        updated = True
        data = {
            'id': obj.id,
            'image': obj.images(),
            'content': obj.contents(),
            'updated':updated,
            'liked':liked
        }
        return Response(data)


class commentcreate(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request,pk,*args, **kwargs):
        posts = get_object_or_404(post,pk=pk)
        serializer_context = {
            'request': request,
        }
        serializer = PostDetails(posts,context=serializer_context)
        return Response(serializer.data, status=200)

    def post(self, request, pk, *args, **kwargs):
        profile = Profiles.objects.get(user=request.user)
        posts = get_object_or_404(post, id=pk)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=profile, post=posts)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

# class commentDetails(RetrieveAPIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = Comment.objects.all()
#     serializer_class = CommentDetails
#     lookup_field='pk'


class commentList(ListAPIView):
    queryset = Comment.objects.filter(reply=None)
    serializer_class = CommentList
    permission_classes = [IsAuthenticated]
    lookup_field='pk'

class commentDetails(DestroyModelMixin,UpdateModelMixin,RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetails
    permission_classes = [IsAuthenticated]

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


    



