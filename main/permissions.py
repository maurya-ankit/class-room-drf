from rest_framework import permissions
from .models import Membership,Classroom
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author == request.user


class ClassroomOwnerOrReadOnly(permissions.BasePermission):
    message = 'You havn\'t joined this classroom'
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        members = Membership.objects.filter(classroom=obj,is_Admin=True)
        for member in members:
            if member.person == request.user:
                return True
        return False
