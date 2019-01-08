from rest_framework.relations import PrimaryKeyRelatedField

from django.core.exceptions import ObjectDoesNotExist


class GetOrCreatePrimaryKeyRelatedField(PrimaryKeyRelatedField):
    """Field creates related object if not found"""

    def __init__(self, **kwargs):
        self.model = kwargs.pop('model')
        super(GetOrCreatePrimaryKeyRelatedField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        """Overrides method to create object if not found"""

        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        try:
            return self.get_queryset().get(pk=data)
        except ObjectDoesNotExist:
            return self.model.objects.create(pk=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)