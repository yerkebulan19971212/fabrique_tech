from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    TEXT = 'TEXT'
    CHOICE = 'CHOICE'
    MULTICHOICE = 'MULTICHOICE'

    CHOICES = (
        (TEXT, 'TEXT'),
        (CHOICE, 'CHOICE'),
        (MULTICHOICE, 'MULTICHOICE'),
    )

    poll = models.ForeignKey(Poll, related_name="questions",
                             on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    type = models.CharField(
        max_length=11, choices=CHOICES, default=TEXT
    )

    def __str__(self):
        return " ".join([self.poll.title, self.text, self.type])


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name='choices', on_delete=models.CASCADE
    )
    text = models.CharField(max_length=256, default='Enter a value')

    def __str__(self):
        return " ".join([self.question.text, self.text])


class PassedPoll(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    anonymous = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    passed_poll = models.ForeignKey(PassedPoll, related_name='answers',
                                    on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question',
                                 on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice, related_name='choices',
                                     blank=True)
    choice_text = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return " ".join([self.question.text])
