from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from scholarships import Scholarship
from applications.models import Application
from notifications.services import create_notification

class Command(BaseCommand):
    help = 'Send deadline reminders for upcoming scholarship applications'
    
    def handle(self, *args, **options):
        today = timezone.now().date()
        deadline_approaching = today + timedelta(days=7)
        
        # Find scholarships with deadlines in 7 days
        upcoming_deadlines = Scholarship.objects.filter(
            is_active=True,
            application_end_date=deadline_approaching
        )
        
        # Find draft applications for these scholarships and send reminders
        for scholarship in upcoming_deadlines:
            draft_applications = Application.objects.filter(
                scholarship=scholarship,
                status='draft'
            )
            
            for application in draft_applications:
                create_notification(
                    user=application.user,
                    title="Application Deadline Reminder",
                    message=f"The deadline for '{scholarship.title}' scholarship is in 7 days. Don't forget to complete and submit your application.",
                    notification_type='deadline',
                    related_link=f"/applications/{application.id}/edit"
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Sent reminder to {application.user.email} for {scholarship.title}"
                    )
                )