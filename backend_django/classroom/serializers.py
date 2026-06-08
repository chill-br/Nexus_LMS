from rest_framework import serializers
from .models import Course, Post, Enrollment
from django.contrib.auth import get_user_model

User = get_user_model()

class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.ReadOnlyField(source='teacher.username')
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'section', 'description', 'invite_code', 'theme_color', 'teacher_name', 'created_at']
        read_only_fields = ['invite_code']

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'course', 'author', 'author_name', 'content', 'attachments', 'created_at']
        read_only_fields = ['author']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at']
