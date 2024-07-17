from django.contrib import admin

from polls.models import Poll, PollAnswer, PollResults

admin.site.register(Poll)
admin.site.register(PollAnswer)
admin.site.register(PollResults)

__all__ = ["admin"]
