from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import PollSerializer
from .models import Poll


class PollModelViewSet(ModelViewSet):
    queryset = Poll.objects.all().prefetch_related('questions')
    serializer_class = PollSerializer
