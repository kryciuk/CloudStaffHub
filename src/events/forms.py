from django.forms import ModelForm

from events.models import Assignment


class AssigmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = "__all__"
        exclude = ["manager", "status"]
        labels = {"name": "Name", "event_date": "Deadline", "employee": "Assigned Employees"}


class AssigmentStatusForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ["status"]
