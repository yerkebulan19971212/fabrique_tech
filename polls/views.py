from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet

from .models import PassedPoll, Poll, Question
from .serializers import (PassedPollSerializer, PollSerializer,
                          QuestionSerializer, UserPassedPollSerializer)


class PollModelViewSet(ModelViewSet):

    queryset = Poll.objects.all().prefetch_related('questions')
    serializer_class = PollSerializer


class QuestionModelViewSet(ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class PassPollView(CreateAPIView):
    serializer_class = PassedPollSerializer


class UserPassedPollView(ListAPIView):
    queryset = PassedPoll.objects.all().prefetch_related(
        'answers', 'answers__choices'
    )
    serializer_class = UserPassedPollSerializer

#     serializer_class = PassPollSerializer
#
#     def post(self, request, *args, **kwargs):
#         user_id = request.user.pk
#         anonymous = False
#         if not user_id:
#             anonymous = True
#             bit_size = 100
#             sized_unique_id = uuid4().int >> bit_size
#             user_id = sized_unique_id
#
#         poll = request.data.get('poll')
#         questions = request.data.get('questions')
#         for q in questions:
#             choices = q.get('choices', [])
#             choice_text = q.get('choice_text', None)
#             answer = Answer.objects.create(
#                 user_id=user_id, poll_id=poll, question_id=q.get('pk'),
#                 choice_text=choice_text, anonymous=anonymous
#             )
#             if choices:
#                 answer.choices.add(*[c.get('pk') for c in choices])
#
#         return Response({"asd"})
#
#
# class UserPollView(ListAPIView):
#
#     queryset = Answer.objects.all()
#     serializer_class = UserPassPollSerializer
#     lookup_field = 'user_id'
#
#     def get_queryset(self):
#         return self.queryset.filter(user_id=self.kwargs['user_id'])

    # def get(self, request, *args, **kwargs):
    #     q = self.get_queryset().values('poll_id').annotate()
    #     return Response("")
    #     return self.list(request, *args, **kwargs)
