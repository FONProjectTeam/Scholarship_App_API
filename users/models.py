from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save



from django.dispatch import receiver
from shortuuid.django_fields import ShortUUIDField

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Administrator'),
        ('reviewer', 'Reviewer'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    other_name = models.CharField(max_length=150, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True, blank=True)

    state_of_origin = models.CharField(max_length=50, blank=True)
    lga_of_origin = models.CharField(max_length=100, blank=True)

    otp = models.CharField(max_length=100, blank=True, null=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    #Create username from email
    def save(self, *args, **kwargs):
        if not self.username:
            try:
                self.username = self.email.split('@')[0]
            except:
                self.username = self.first_name

        super().save(*args, **kwargs)
        

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    lcda = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default="default/default-profile.jpg", null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    education_level = models.CharField(max_length=100, blank=True, null=True)
    institution = models.CharField(max_length=255, blank=True, null=True)
    major = models.CharField(max_length=255, blank=True, null=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='0123456789')

    def __str__(self):
        full_name = self.user.get_full_name()
        if full_name:
            return f"{full_name}'s Profile"
        else:
            return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)        
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
