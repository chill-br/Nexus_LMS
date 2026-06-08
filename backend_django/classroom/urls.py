from django.urls import path
from .views import CourseListCreateView, JoinCourseView, PostListCreateView, CourseMembersView, CourseGradesView

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/join/', JoinCourseView.as_view(), name='course-join'),
    path('courses/<int:course_id>/posts/', PostListCreateView.as_view(), name='course-posts'),
    path('courses/<int:course_id>/members/', CourseMembersView.as_view(), name='course-members'),
    path('courses/<int:course_id>/grades/', CourseGradesView.as_view(), name='course-grades'),
]
