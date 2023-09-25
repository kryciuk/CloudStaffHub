from django.forms import ModelForm
from polls.models import Poll, PollAnswer


class PollCreateForm(ModelForm):
    class Meta:
        model = Poll
        fields = "__all__"
        exclude = ["status", "date_created", "created_by"]


class PollCloseForm(ModelForm):
    class Meta:
        model = Poll
        fields = ["status"]


class PollUpdateForm(ModelForm):
    class Meta:
        model = Poll
        fields = ["status"]


class PollAnswerCreateForm(ModelForm):
    class Meta:
        model = PollAnswer
        fields = "__all__"