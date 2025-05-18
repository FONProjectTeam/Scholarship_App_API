from django.db import models
from users.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('application_status', 'Application Status Update'),
        ('deadline', 'Scholarship Deadline'),
        ('document', 'Document Request'),
        ('system', 'System Notification'),
    )
    
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    related_link = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} for {self.user.username}"

class NotificationPreference(models.Model):
    user = models.OneToOneField(User, related_name='notification_preferences', on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    application_updates = models.BooleanField(default=True)
    deadline_reminders = models.BooleanField(default=True)
    document_requests = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"
