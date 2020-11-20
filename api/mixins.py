from django.shortcuts import get_object_or_404
from django.core.exceptions import FieldError
from rest_framework.response import Response

from .models import Cafe


class PermittedCafeMixin:
    '''This project uses model permissions,
    but employees from different cafes should not
    be able to edit info about other cafes as well.
    This mixin provides a few utility methods for
    that purpose. '''

    def get_permitted_queryset(self):
        '''This method was changed so that employee can't edit
         or delete products from other cafes'''
        cafe = self.request.user.employee.cafe
        try:
            return self.queryset.filter(cafe=cafe)
        except FieldError:
            return self.queryset.filter(pk=cafe.pk)

    def get_permitted_object(self):
        '''The first line is changed'''
        queryset = self.filter_queryset(self.get_permitted_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj

    def permitted_update(self, request, *args, **kwargs):
        '''Like the regular DRF update method, but with
        changed self.get_permitted_object '''
        partial = kwargs.pop('partial', False)
        instance = self.get_permitted_object()  # This line is changed
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
