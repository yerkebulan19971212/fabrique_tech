from rest_framework import serializers
from polls.models import Poll, Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ('id', 'text')
        read_only_fields = ('id', )


class QuestionSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=Question.CHOICES, default=Question.TEXT
    )
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'poll', 'text', 'type', 'choices')
        read_only_fields = ('id',)
        extra_kwargs = {
            'poll': {'write_only': True}
        }

    def create_choices(self, question, choices):
        Choice.objects.bulk_create([
            Choice(question=question, **d) for d in choices
        ])

    def create(self, validated_data):
        choices = validated_data.pop('choices', [])
        question = Question.objects.create(**validated_data)
        self.create_choices(question, choices)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices', [])
        instance.choices.all().delete()
        self.create_choices(instance, choices)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


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

