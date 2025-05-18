from rest_framework import serializers
from applications.models import Application, Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    scholarship_title = serializers.ReadOnlyField(source='scholarship.title')
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['user', 'status', 'submission_date', 'created_at', 'updated_at']