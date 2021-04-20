from rest_framework import serializers

from polls.models import Answer, Choice, PassedPoll, Poll, Question


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ('id', 'text')


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
        fields = (
            'pk', 'title', 'start_date', 'end_date', 'description',
            'questions'
        )
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


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id', 'question', 'choices', 'choice_text')


class PassedPollSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = PassedPoll
        fields = ('id', 'poll', 'user_id', 'anonymous', 'created', 'answers')
        read_only_fields = ('id', 'user_id', 'created')

    def create(self, validated_data):
        answers = validated_data.pop('answers', [])
        instance = self.Meta.model.objects.create(**validated_data, user_id=1)
        for a in answers:
            choice_text = a.get('choice_text', None)
            answer = Answer.objects.create(
                passed_poll=instance,
                choice_text=choice_text,
                question=a.get("question"),
            )
            choices = a.get('choices')
            if choices:
                answer.choices.add(*[c for c in choices])
        return instance


class ReadAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Answer
        fields = ('id', 'question', 'choices', 'choice_text')


class UserPassedPollSerializer(serializers.ModelSerializer):
    answers = ReadAnswerSerializer(many=True)

    class Meta:
        model = PassedPoll
        fields = ('id', 'poll',  'created', 'answers')
