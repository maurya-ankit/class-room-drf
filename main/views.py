from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.contrib.auth.models import User
from .models import ClassroomPost,ClassroomPostComment,Classroom,Membership
from . import serializers
from rest_framework.response import Response
from  .permissions import IsOwnerOrReadOnly,ClassroomOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.exceptions import ValidationError,ParseError

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ClassroomList(generics.ListCreateAPIView):
    # queryset = Classroom.objects.all()
    serializer_class = serializers.ClassroomSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        ClassroomOwnerOrReadOnly,
        ]

    def perform_create(self,serializer):
        obj = serializer.save()
        Membership(person=self.request.user,is_Admin=True,classroom=obj).save()

    def get_queryset(self):
        queryset = Classroom.objects.filter(members = self.request.user)
         
        if len(queryset):
            return queryset
        else:
            raise ValidationError(detail='Invalid Params')


class ClassroomDetail(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = serializers.ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated,ClassroomOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Classroom.objects.all()
        return queryset.filter(members = self.request.user)



class MembershipList(generics.ListCreateAPIView):
    # queryset = Membership.objects.all()
    serializer_class = serializers.MembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Membership.objects.all()
        # Getting classroom id from query parameters in url -> "/?classroom=1"
        classroom = self.request.query_params.get('classroom', None)
        if classroom is not None:
            queryset = queryset.filter(classroom__pk=classroom)
        else:
            queryset = Membership.objects.none()
        
        status = False
        for q in queryset:
            if q.person==self.request.user:
                status = True
                break

        
        return queryset if status else Membership.objects.none()


class MembershipDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Membership.objects.all()
    serializer_class = serializers.MembershipSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        ]
        
    def get_queryset(self):
        queryset = Membership.objects.all()
        # Getting classroom id from query parameters in url -> "/?classroom=1"
        classroom = self.request.query_params.get('classroom', None)
        if classroom is not None:
            queryset = queryset.filter(classroom__pk=classroom)
        else:
            queryset = Membership.objects.none()
        
        status = False
        for q in queryset:
            if q.person==self.request.user:
                status = True
                break

        
        return queryset if status else Membership.objects.none()





class ClassroomPostList(generics.ListCreateAPIView):
    serializer_class = serializers.ClassroomPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # cpk = None if self.request.data.get('classroom')==None else self.request.data.get('classroom')
        classroom = self.request.query_params.get('classroom', None)
        if classroom is not None:
            obj = Classroom.objects.filter(pk=classroom).first()
            serializer.save(author=self.request.user,classroom=obj)
        else:
            raise ParseError(detail="classroom id not available")
        
    def get_queryset(self):
        queryset = ClassroomPost.objects.all()
        # Getting classroom id from query parameters in url -> "/?classroom=1"
        classroom = self.request.query_params.get('classroom', None)
        if classroom is not None:
            queryset = queryset.filter(classroom__pk=classroom)
        else:
            queryset = Membership.objects.none()

        is_member = bool(len(Membership.objects.filter(classroom__pk=classroom,person=self.request.user)))

        return queryset if is_member else ClassroomPost.objects.none()



class ClassroomPostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ClassroomPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = ClassroomPost.objects.all()
        # Getting classroom id from query parameters in url -> "/?classroom=1"
        classroom = self.request.query_params.get('classroom', None)
        if classroom is not None:
            queryset = queryset.filter(classroom__pk=classroom)
        else:
            queryset = Membership.objects.none()

        is_member = bool(len(Membership.objects.filter(classroom__pk=classroom,person=self.request.user)))

        return queryset if is_member else ClassroomPost.objects.none()




class ClassroomPostCommentList(generics.ListCreateAPIView):
    queryset = ClassroomPostComment.objects.all()
    serializer_class = serializers.ClassroomPostCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)


class ClassroomPostCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassroomPostComment.objects.all()
    serializer_class = serializers.ClassroomPostCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


from rest_framework import viewsets
class ClassroomViewSet(viewsets.ModelViewSet):
    queryset= ClassroomPost.objects.all()
    serializer_class=serializers.ClassroomPostSerializer