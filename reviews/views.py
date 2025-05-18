from django.shortcuts import render

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import ReviewSerializer
from reviews.models import Review
from applications.models import Application
from notifications.models import Notification
from api.permissions import IsAdminOrReviewer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReviewer]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Review.objects.all()
        elif user.user_type == 'reviewer':
            return Review.objects.filter(reviewer=user)
        return Review.objects.none()
    
    def perform_create(self, serializer):
        review = serializer.save(reviewer=self.request.user)
        
        # Update application status based on review
        application = review.application
        recommendation = review.recommendation
        
        if recommendation == 'approve':
            application.status = 'approved'
        elif recommendation == 'reject':
            application.status = 'rejected'
        elif recommendation == 'more_info':
            application.status = 'additional_info'
        
        application.save()
        
        # Create notification for the applicant
        notification_message = f"Your application for {application.scholarship.title} has been reviewed."
        if recommendation == 'more_info':
            notification_message += " Additional information is required."
        
        Notification.objects.create(
            user=application.user,
            title=f"Application {application.status.replace('_', ' ').title()}",
            message=notification_message,
            notification_type='application_status',
            related_link=f"/applications/{application.id}/"
        )
