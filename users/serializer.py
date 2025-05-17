from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User, UserProfile

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name        

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'other_name', 'phone_number', 'email', 'state_of_origin', 'lga_of_origin',  'password', 'password2']


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            other_name=validated_data['other_name'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
        )

        user.username = user.email.split('@')[0] 
        user.set_password(validated_data['password'])
        user.save()
        return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        #read_only_fields = ['id']
        
    
class UserProfileSerializer(serializers.ModelSerializer):
    #user = UserSerializer #(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = "__all__"
        #read_only_fields = ['id', 'user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation