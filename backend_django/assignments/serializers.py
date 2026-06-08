from rest_framework import serializers
from .models import Assignment, Submission

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'course', 'title', 'instructions', 'attachments', 'due_date', 'created_at']

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'student', 'student_name', 'file', 'submitted_at', 'status', 'grade', 'ai_feedback']
        read_only_fields = ['student', 'status', 'ai_feedback']
