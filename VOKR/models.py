from django.db import models
from django.utils import timezone

class Company(models.Model):
    # Django automatically adds a primary key field named "id"
    name = models.CharField(max_length=255, unique=True)  # Ensuring company names are unique

    def __str__(self):
        return self.name

class File(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='files')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)  # e.g., 'pdf', 'docx', etc.
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=500)  # Path where the file is stored

    def __str__(self):
        return f"{self.file_name} ({self.company.name})"

class Session(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_accessed_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.session_id


class Message(models.Model):
    USER_ROLE = 'user'
    ASSISTANT_ROLE = 'assistant'
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    sent_timestamp = models.DateTimeField(default=timezone.now)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    message = models.TextField()

    def __str__(self):
        return f"{self.role}: {self.message[:50]}..."