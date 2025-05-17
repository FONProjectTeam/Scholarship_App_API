from django.db import models
from users.models import User

class ScholarshipCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Scholarship Categories"

class Scholarship(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ScholarshipCategory, related_name='scholarships', on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, related_name='created_scholarships', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    application_start_date = models.DateField()
    application_end_date = models.DateField()
    requirements = models.TextField()
    eligibility_criteria = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
        
    @property
    def is_open(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.is_active and self.application_start_date <= today <= self.application_end_date