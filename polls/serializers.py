from rest_framework import serializers
from polls.models import Poll, Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Choice serializer.
    """
    class Meta:
        model = Choice
        fields = ('id', 'text')
        read_only_fields = ('id', )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ('id',)
        extra_kwargs = {
            'poll': {'write_only': True}
        }


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('pk', 'title', 'start_date', 'end_date', 'description', 'questions')
        read_only_fields = ('pk', )

    def validate_start_date(self, value):
        """
        Raise error if try to change start_date after poll started.
        """
        if self.instance and (self.instance.start_date < value or
                              self.instance.start_date > value):
            raise serializers.ValidationError(
                'After creation, the field start_date for the poll cannot be changed'
            )

        return value

