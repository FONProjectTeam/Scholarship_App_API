from django.shortcuts import render

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from scholarships.serializers import ScholarshipSerializer, ScholarshipCategorySerializer
from scholarships.models import Scholarship, ScholarshipCategory
from api.permissions import IsAdminOrReadOnly

class ScholarshipViewSet(viewsets.ModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['application_end_date', 'created_at', 'amount']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ScholarshipCategoryViewSet(viewsets.ModelViewSet):
    queryset = ScholarshipCategory.objects.all()
    serializer_class = ScholarshipCategorySerializer
    permission_classes = [IsAdminOrReadOnly]