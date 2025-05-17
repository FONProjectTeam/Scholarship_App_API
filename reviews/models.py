from django.db import models
from users.models import User
from applications.models import Application

class Review(models.Model):
    application = models.ForeignKey(Application, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)  # Can be used for numeric evaluation
    comments = models.TextField()
    recommendation = models.CharField(max_length=20, choices=[
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('more_info', 'Request More Information'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('application', 'reviewer')
    
    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.application}"
