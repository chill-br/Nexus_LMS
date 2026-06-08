from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from .classroom.models import Course, Enrollment, Post
from .classroom.serializers import CourseSerializer, PostSerializer
from .users.serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# --- AUTH LOGIC ---

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class LoginView(TokenObtainPairView):
    # Standard SimpleJWT login
    pass

# --- COURSE LOGIC ---

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
            return Response({"error": "Invite code required"}, status=status.HTTP_400_BAD_REQUEST)
        
        course = get_object_or_404(Course, invite_code=invite_code)
        
        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return Response({"message": "Already enrolled"}, status=status.HTTP_200_OK)
            
        Enrollment.objects.create(user=request.user, course=course)
        return Response({"message": "Successfully joined course", "course": course.name}, status=status.HTTP_201_CREATED)

# --- TABS LOGIC ---

class CoursePostsView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(course_id=self.kwargs['course_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, course_id=self.kwargs['course_id'])
