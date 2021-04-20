from django.contrib import admin
from .models import Question, Poll

admin.site.register([Question, Poll])

# Register your models here.
