from django.db import models
from django.conf import settings
from django.utils import timezone
from classroom.models import Course

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    attachments = models.FileField(upload_to='assignments/', null=True, blank=True)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Submission(models.Model):
    class Status(models.TextChoices):
        TURNED_IN = 'TURNED_IN', 'Turned In'
        LATE = 'LATE', 'Late'
        MISSING = 'MISSING', 'Missing'

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='submissions'
    )
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.TURNED_IN)
    grade = models.FloatField(null=True, blank=True)
    ai_feedback = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Basic check for late submission
        if not self.id and hasattr(self, 'assignment') and self.assignment.due_date:
            if timezone.now() > self.assignment.due_date:
                self.status = self.Status.LATE
        super().save(*args, **kwargs)
