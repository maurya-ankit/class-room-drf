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
         
        return queryset


class ClassroomDetail(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = serializers.ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated,ClassroomOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Classroom.objects.all()
        return queryset.filter(members = self.request.user)



class MembershipList(generics.ListCreateAPIView):
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
            raise ParseError(detail="Classroom id not available")
        
        status = False
        for q in queryset:
            if q.person==self.request.user:
                status = True
                break

        if status:
            return queryset
        else:
            raise ParseError(detail="You are not a member")



class MembershipDetail(generics.RetrieveUpdateDestroyAPIView):
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
            raise ParseError(detail="Classroom id not available")

        
        status = False
        for q in queryset:
            if q.person==self.request.user:
                status = True
                break

        if status:
            return queryset
        else:
            raise ParseError(detail="You are not a member")
        





class ClassroomPostList(generics.ListCreateAPIView):
    serializer_class = serializers.ClassroomPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        '''
        retrieving query parameter from request url, querying for Classroom object.
        if it's empty -> user havn't joned classroom...
        '''
        classroom = self.request.query_params.get('classroom', None)
        if classroom is not None:
            obj = Classroom.objects.filter(pk=classroom,members=self.request.user).first()
            try:
                serializer.save(author=self.request.user,classroom=obj)
            except:
                raise ParseError(detail="You are not a member of this classroom")
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
            raise ParseError(detail="classroom id not available")

        is_member = bool(len(Classroom.objects.filter(pk=classroom,members=self.request.user)))
        if is_member:
            return queryset
        else:
            raise ParseError(detail="no posts or you are not a member")

        # return queryset if is_member else ClassroomPost.objects.none()



class ClassroomPostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ClassroomPostSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = ClassroomPost.objects.all()
        # Getting classroom id from query parameters in url -> "/?classroom=1"
        classroom = self.request.query_params.get('classroom', None)
        if classroom is not None:
            queryset = queryset.filter(classroom__pk=classroom)
        else:
            queryset = Membership.objects.none()
            raise ParseError(detail="classroom id not available")

        is_member = bool(len(Membership.objects.filter(classroom__pk=classroom,person=self.request.user)))

        return queryset if is_member else ClassroomPost.objects.none()




class ClassroomPostCommentList(generics.ListCreateAPIView):
    serializer_class = serializers.ClassroomPostCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def perform_create(self,serializer):
    #     serializer.save(author=self.request.user)
    def perform_create(self, serializer):
        classroom = self.request.query_params.get('classroom', None)
        post = self.request.query_params.get('post',None)
        if classroom is None:
            raise ParseError(detail="classroom id not available")
        elif post is None:
            raise ParseError(detail="post id not available")
        else:
            classroom_obj = Classroom.objects.filter(pk=classroom,members=self.request.user)
            if not len(classroom_obj):
                raise ParseError(detail="you are not a member of this classroom")
            
            post_obj = ClassroomPost.objects.filter(pk=post,classroom__pk=classroom).first()
            serializer.save(author=self.request.user,classroom_post=post_obj)

    def get_queryset(self):
        queryset = ClassroomPostComment.objects.all()
        classroom = self.request.query_params.get('classroom', None)
        post = self.request.query_params.get('post',None)
        if classroom is None:
            raise ParseError(detail="classroom id not available")
        elif post is None:
            raise ParseError(detail="post id not available")
        else:
            classroom_obj = Classroom.objects.filter(pk=classroom,members=self.request.user)
            if not len(classroom_obj):
                raise ParseError(detail="you are not a member of this classroom")
            is_classroomPost = len(ClassroomPost.objects.filter(classroom__pk=classroom))
            if is_classroomPost:
                return queryset.filter(classroom_post__pk=post,classroom_post__classroom__pk=classroom)
            else:
                raise ParseError(detail="not a post of this classroom")




class ClassroomPostCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassroomPostComment.objects.all()
    serializer_class = serializers.ClassroomPostCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

