from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User Model

    Notes
    -----
    Customizations:
    1. user 'id' field is declared to be read only field. It will be
    auto-created by model and returned as response but not in request

    2. password is write only field. It will be written to model but won't
    be in response, for security reasons

    3. 'is_staff' field is added to define if user is admin(staff member)
    or not.
    """

    class Meta:
        """Meta class for UserSerializer"""

        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email',
                  'is_staff', 'id')
        read_only_fields = ('id',)
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
        return attrs

    def create(self, validated_data):
        """Uses 'create_user' instead of 'create' to create User

        Notes
        -----
        Generic 'create' method doesn't perform some important tasks
        required to create user.
        'create_user' sets up the password, normalize username and email
        before saving to DB.
        """

        return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer to change User password

    Fields
    ------

        old_password -  Old user password that's to be replaced
        new_password -  New user password. should be large than 8 chars
    """

    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128, min_length=8)
