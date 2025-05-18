from rest_framework import serializers
from scholarships.models import Scholarship, ScholarshipCategory

class ScholarshipCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScholarshipCategory
        fields = '__all__'

class ScholarshipSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    is_open = serializers.ReadOnlyField()
    
    class Meta:
        model = Scholarship
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']