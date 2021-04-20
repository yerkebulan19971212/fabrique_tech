from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import PollSerializer, QuestionSerializer
from .models import Poll, Question


class PollModelViewSet(ModelViewSet):

    queryset = Poll.objects.all().prefetch_related('questions')
    serializer_class = PollSerializer


class QuestionModelViewSet(ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
