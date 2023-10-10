from django.forms import ModelForm
from polls.models import Poll, PollAnswer
from datetime import date


class PollCreateForm(ModelForm):
    class Meta:
        model = Poll
        fields = "__all__"
        exclude = ["status", "date_created", "created_by"]

    def clean(self):
        cleaned_data = super().clean()

        today = date.today()
        date_end = cleaned_data.get("date_end")

        if today > date_end:
            msg = "The end date must be later than today's date."
            self.add_error('date_end', msg)


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
