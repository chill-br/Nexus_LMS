from django.db import models
from django.conf import settings
from classroom.models import Course

class KnowledgeBase(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='knowledge_base')
    vector_id = models.CharField(max_length=255, help_text="ID reference in the vector database index")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"KB for {self.course.name}"

class ChatLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    query = models.TextField()
    response = models.TextField()
    concept_tags = models.JSONField(default=list, help_text="Extracted concepts for teacher analytics")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat by {self.user.username} in {self.course.name}"
