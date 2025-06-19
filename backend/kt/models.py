import uuid
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class KTSession(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User , on_delete=models.CASCADE , related_name='kt_sessions')
    share_token = models.UUIDField(default=uuid.uuid4, unique=True , editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    

class Attachment(models.Model):
    FILE_TYPE_CHOICES = [
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('text', 'Text'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    ]

    session = models.ForeignKey(KTSession, on_delete=models.CASCADE, related_name='attachments')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES) 
    file_url = models.URLField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    transcript = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.session.title} - {self.file_type}"
    
    


