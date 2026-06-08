from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer

class AssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id') or self.request.query_params.get('course_id')
        return Assignment.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        if self.request.user.role != 'TEACHER':
            raise permissions.PermissionDenied("Only teachers can create assignments.")
        course_id = self.kwargs.get('course_id')
        serializer.save(course_id=course_id)

class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
