from django.contrib import admin

from evaluation.models import Answer, Question, Questionnaire

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Questionnaire)
