from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User Model"""

    class Meta:
        """Meta class for UserSerializer"""

        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email',
                  'is_staff')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        """UserSerializer Custom Validation

        Raises
        ------
        <rest_framework.exception.Validation> :
            if password is being updated
        """
        if self.instance and attrs.get('password'):
            raise ValidationError('Password update is not allowed')

    def create(self, validated_data):
        """Uses 'create_user' instead of 'create' to create User"""

        return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer to change User password"""

    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128, min_length=8)
