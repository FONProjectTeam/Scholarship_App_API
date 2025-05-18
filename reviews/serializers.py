from rest_framework import serializers
from reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.ReadOnlyField(source='reviewer.get_full_name')
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['reviewer', 'created_at', 'updated_at']