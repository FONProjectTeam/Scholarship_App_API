from django.shortcuts import render

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from applications.serializers import ApplicationSerializer, DocumentSerializer
from applications.models import Application, Document
from notifications.models import Notification
from api.permissions import IsOwnerOrAdmin

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['admin', 'reviewer']:
            return Application.objects.all()
        return Application.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        application = self.get_object()
        
        # Check if application is already submitted
        if application.status != 'draft':
            return Response({"error": "Only draft applications can be submitted"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Update application status
        application.status = 'submitted'
        application.submission_date = timezone.now()
        application.save()
        
        # Create notification for user
        Notification.objects.create(
            user=application.user,
            title="Application Submitted",
            message=f"Your application for {application.scholarship.title} has been submitted.",
            notification_type='application_status'
        )
        
        return Response({"success": "Application submitted successfully"})

class DocumentViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['admin', 'reviewer']:
            return Document.objects.all()
        return Document.objects.filter(application__user=user)
    
    def perform_create(self, serializer):
        application = serializer.validated_data.get('application')
        if application.user != self.request.user and self.request.user.user_type not in ['admin', 'reviewer']:
            self.permission_denied(self.request)
        serializer.save()
