from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.contrib.auth.models import User
from .models import ClassroomPost,ClassroomPostComment,Classroom,Membership
from . import serializers
from rest_framework.response import Response
from  .permissions import IsOwnerOrReadOnly,ClassroomOwnerOrReadOnly
from rest_framework import permissions

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ClassroomList(generics.ListCreateAPIView):
    # queryset = Classroom.objects.all()
    serializer_class = serializers.ClassroomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self,serializer):
        obj = serializer.save()
        Membership(person=self.request.user,is_Admin=True,classroom=obj).save()

    def get_queryset(self):
        return Classroom.objects.filter(members = self.request.user)


class ClassroomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = serializers.ClassroomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,ClassroomOwnerOrReadOnly]


class MembershipList(generics.ListCreateAPIView):
    # queryset = Membership.objects.all()
    serializer_class = serializers.MembershipSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Membership.objects.filter(person=self.request.user)


class MembershipDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = serializers.MembershipSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,ClassroomOwnerOrReadOnly]




class ClassroomPostList(generics.ListCreateAPIView):
    queryset = ClassroomPost.objects.all()
    serializer_class = serializers.ClassroomPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        cpk = None if self.request.data.get('classroom')==None else self.request.data.get('classroom')
        classroom = Classroom.objects.filter(pk=cpk).first()
        serializer.save(author=self.request.user,classroom=classroom)

class ClassroomPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassroomPost.objects.all()
    serializer_class = serializers.ClassroomPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


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