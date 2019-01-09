from rest_framework.mixins import UpdateModelMixin


class PartialUpdateMixin(UpdateModelMixin):
    """Mixin to partially update the PUT request."""

    def put(self, request, *args, **kwargs):
        """
        Over-riding `get_serializer`.

        All PUT/PATCH requests will be `partial`, ie only those fields are
        updated which are provided in the request body.
        Rest will remain unchanged.
        """
        return self.partial_update(request, *args, **kwargs)
