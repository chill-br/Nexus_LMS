from django.urls import path
from .views import AssignmentListCreateView, SubmissionCreateView

urlpatterns = [
    path('courses/<int:course_id>/assignments/', AssignmentListCreateView.as_view(), name='assignment-list-create'),
    path('submissions/', SubmissionCreateView.as_view(), name='submission-create'),
]
