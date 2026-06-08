from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Enrollment, Post
from .serializers import CourseSerializer, PostSerializer
from users.serializers import UserSerializer
from django.shortcuts import get_object_or_404

class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'TEACHER':
            return Course.objects.filter(teacher=user)
        return Course.objects.filter(students__user=user)

    def perform_create(self, serializer):
        if self.request.user.role != 'TEACHER':
            raise permissions.PermissionDenied("Only teachers can create courses.")
        serializer.save(teacher=self.request.user)

class JoinCourseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        invite_code = request.data.get('invite_code')
        if not invite_code:
            return Response({"error": "Invite code is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        course = get_object_or_404(Course, invite_code=invite_code)
        
        # Check if already enrolled
        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return Response({"message": "Already enrolled in this course"}, status=status.HTTP_200_OK)
        
        Enrollment.objects.create(user=request.user, course=course)
        return Response({"message": f"Successfully joined {course.name}", "course_id": course.id}, status=status.HTTP_201_CREATED)

class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id') or self.request.query_params.get('course_id')
        return Post.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        post = serializer.save(author=self.request.user, course_id=course_id)
        # In a real RAG app, you'd trigger a background task here 
        # to summarize the announcement for students.
        print(f"Triggering AI summary for post {post.id}")

class CourseMembersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        teacher = UserSerializer(course.teacher).data
        students = UserSerializer([e.user for e in course.students.all()], many=True).data
        return Response({
            "teacher": teacher,
            "students": students
        })

from assignments.models import Submission
from assignments.serializers import SubmissionSerializer

class CourseGradesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, course_id):
        if request.user.role != 'TEACHER':
            return Response({"error": "Only teachers can view grades"}, status=status.HTTP_403_FORBIDDEN)
        
        submissions = Submission.objects.filter(assignment__course_id=course_id)
        return Response(SubmissionSerializer(submissions, many=True).data)
