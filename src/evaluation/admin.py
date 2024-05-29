from django.contrib import admin

from evaluation.models import Answer, Evaluation, Question, Questionnaire

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Questionnaire)
admin.site.register(Evaluation)

__all__ = ["admin"]
