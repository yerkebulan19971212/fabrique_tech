from django.contrib import admin

from .models import Answer, Choice, PassedPoll, Poll, Question

admin.site.register([Question, Poll, Answer, PassedPoll, Choice])
