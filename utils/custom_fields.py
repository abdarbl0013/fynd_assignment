from rest_framework.relations import PrimaryKeyRelatedField


class GetOrCreatePrimaryKeyRelatedField(PrimaryKeyRelatedField):
    """Custom PrimaryRelatedField
    
    Notes
    -----
    If primary value provided doesn't exist in DB,
    Field creates related object with primary key
    """

    def __init__(self, **kwargs):
        self.model = kwargs.pop('model')
        super(GetOrCreatePrimaryKeyRelatedField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        """Overrides method to create object if not found"""

        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        try:
            instance, _ = self.model.objects.get_or_create(pk=data)
            return instance
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)
