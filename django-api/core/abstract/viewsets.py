from rest_framework import viewsets
from rest_framework import filters


class AbstractViewSet(viewsets.ModelViewSet):
    filter_backends = [filter.OrderingFilter]
    ordering_fields = ["updated", "created"]
    ordering = ["-updated"]
