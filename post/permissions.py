from rest_framework.permissions import BasePermission,SAFE_METHODS
from rest_framework import permissions

class IsOwnerOrReadOnly(BasePermission):
      def has_object_permission(self, request, view, obj):
          try:
            return obj.author.user == request.user
          except:
            return obj.user == request.user


class UserOwnerOrReadOnly(BasePermission):
      # def has_object_permission(self, request, view, obj):
      #     #print(obj.user)
      #     print(request.user)
      #     return obj.username == request.user

    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return obj.id == request.user.id

            
            
