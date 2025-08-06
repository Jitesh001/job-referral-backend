from typing import Dict, Type
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response


# Create your models here.
class AbstractTrack(models.Model):
    uuid = models.UUIDField(_("uuid field"), unique=True, default=uuid4, editable=False)
    created = models.DateTimeField(_("created at"), auto_now_add=True)
    modified = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        abstract = True


class ListDetailViewSet(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        response = {"message": "Create function is not offered in this path."}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        response = {"message": "Update function is not offered in this path."}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        response = {"message": "Delete function is not offered in this path."}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ListDetailUpdateViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        response = {"message": "Create function is not offered in this path."}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        response = {"message": "Delete function is not offered in this path."}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ABSViewSet(viewsets.ModelViewSet):
    """
    Action Based Serializers ViewSet
    """

    action_serializers: Dict[str, Type[serializers.Serializer]] = {}

    def get_serializer_class(self):
        if self.action in self.action_serializers:
            return self.action_serializers[self.action]
        return self.serializer_class
