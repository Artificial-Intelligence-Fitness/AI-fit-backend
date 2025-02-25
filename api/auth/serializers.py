from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is not sent back

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Only these fields are allowed

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Hashes password automatically
        return user
