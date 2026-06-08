import random
import string
import uuid
from django.db import models
from django.conf import settings

def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Course(models.Model):
    name = models.CharField(max_length=255)
    section = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='taught_courses'
    )
    invite_code = models.CharField(max_length=6, unique=True, default=generate_invite_code)
    theme_color = models.CharField(max_length=7, default="#4285F4") # Google Blue
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = generate_invite_code()
            # Ensure uniqueness
            while Course.objects.filter(invite_code=self.invite_code).exists():
                self.invite_code = generate_invite_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    """Stream Announcements"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    attachments = models.FileField(upload_to='announcements/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='students'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
