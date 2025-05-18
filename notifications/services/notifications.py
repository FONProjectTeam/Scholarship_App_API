from django.core.mail import send_mail
from django.conf import settings
from notifications.models import Notification, NotificationPreference

def create_notification(user, title, message, notification_type, related_link=None):
    """
    Create an in-app notification and send email if user has enabled it.
    """
    # Create in-app notification
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        related_link=related_link
    )
    
    # Check if user wants email notifications
    try:
        preferences = NotificationPreference.objects.get(user=user)
        
        # Check if this notification type should be emailed
        should_email = False
        if notification_type == 'application_status' and preferences.application_updates:
            should_email = True
        elif notification_type == 'deadline' and preferences.deadline_reminders:
            should_email = True
        elif notification_type == 'document' and preferences.document_requests:
            should_email = True
        
        if preferences.email_notifications and should_email:
            send_email_notification(user.email, title, message)
    
    except NotificationPreference.DoesNotExist:
        # Default to sending emails if preferences not set
        send_email_notification(user.email, title, message)
    
    return notification

def send_email_notification(email, subject, message):
    """
    Send an email notification to a user.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email]
    )