from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from .serializers import ProfilesList,ProfilesUpdate,UserList,UpdateUserSerializer
from rest_framework import generics
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,RetrieveUpdateAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profiles
from post.permissions import IsOwnerOrReadOnly,UserOwnerOrReadOnly

# class ProfilesApi(RetrieveAPIView):
#     queryset = Profiles.objects.all().order_by('-id')
#     serializer_class = ProfilesList
#     lookup_field='user__username'

class ProfilesApi(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ProfilesList
    permission_classes = [IsAuthenticated]

    def get(self, request,username,*args, **kwargs):
        profile = get_object_or_404(Profiles,user__username=username)
        serializer_context = {
            'request': request,
        }
        serializer = self.serializer_class(profile,context=serializer_context)
        return Response(serializer.data, status=200)
    

class ProfilesUpdateApi(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated,UserOwnerOrReadOnly]
    lookup_field=('username')
    #print(lookup_field)

    # def perform_update(self,serializer):
    #     serializer.save(user=self.request.user)
