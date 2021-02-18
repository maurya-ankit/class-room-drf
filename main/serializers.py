from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # classroomposts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # comment = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            # 'classroomposts',
            # 'comment',
            'password'
            ]
        model = User


class ClassroomSerializer(serializers.ModelSerializer):
    total_members = serializers.ReadOnlyField()
    class Meta:
        model = models.Classroom
        fields = [
            'id',
            'name',
            'created_at',
            'total_members'
        ]

class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Membership
        fields = '__all__'


class ClassroomPostSerializer(serializers.ModelSerializer):
    author= serializers.ReadOnlyField(source='author.username')
    comment = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    total_comments = serializers.ReadOnlyField()
    class Meta:
        model = models.ClassroomPost
        # fields = '__all__'
        fields = [
            'title',
            'subtitle',
            'content',
            'attachment',
            'comment',
            'author',
            'total_comments',
            ]


class ClassroomPostCommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = models.ClassroomPostComment
        fields = '__all__'