from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView

from utils.mixins import PartialUpdateMixin
from .serializers import UserSerializer, ChangePasswordSerializer


class UserRegisterView(CreateAPIView):
    """View registers User"""

    serializer_class = UserSerializer


class ChangePasswordView(CreateAPIView):
    """View to change User password
    
    Notes
    -----
    Only authenticated user are allowed to change password.
    """

    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Get User object
        
        Returns
        -------
        <django.contrib.auth.models.User> :
            Authenticated User object
        """
        
        return self.request.user

    def post(self, request, *args, **kwargs):
        """Change User password
        
        Parameters
        ----------
        request : <rest_framework.requests.Request>
            Request Object with data
                {
                    'old_password': 'string',
                    'new_password': 'string1'
                }

        Notes
        -----
        1. Verify old password against Authenticated user
        2. If successfully verified, set new password
        """
        user = self.get_object()

        # Validated request data with serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check old password
        if not user.check_password(serializer.data['old_password']):
            return Response({"old_password": ["Wrong password."]},
                            status=status.HTTP_400_BAD_REQUEST)

        # set_password sets and hashes the password that the user will get
        user.set_password(serializer.data['new_password'])
        user.save()
        return Response("Success.", status=status.HTTP_200_OK)


class UserDetailsView(RetrieveDestroyAPIView, PartialUpdateMixin):
    """View implements Update, Retrieve and Delete operation on User
    
    Notes
    -----
    Only authenticated user are allowed to update, read or delete User details.
    """

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Get User Object.
        
        Returns
        -------
        <django.contrib.auth.models.User> :
            Authenticated User object
        """
        return self.request.user

    def perform_destroy(self, instance):
        """Instance is made inactive instead of deleting."""

        instance.is_active = False
        instance.save()
