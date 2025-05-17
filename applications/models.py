from django.db import models
from users.models import User
from scholarships.models import Scholarship

class Application(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('additional_info', 'Additional Information Required'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship, related_name='applications', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submission_date = models.DateTimeField(null=True, blank=True)
    academic_info = models.TextField(blank=True)
    financial_info = models.TextField(blank=True)
    personal_statement = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'scholarship')
    
    def __str__(self):
        return f"{self.user.username}'s application for {self.scholarship.title}"

class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = (
        ('transcript', 'Academic Transcript'),
        ('id', 'Identification Document'),
        ('rec_letter', 'Recommendation Letter'),
        ('financial', 'Financial Document'),
        ('other', 'Other'),
    )
    
    application = models.ForeignKey(Application, related_name='documents', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='application_documents/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_document_type_display()} for {self.application}"
