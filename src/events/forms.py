from django.forms import ModelForm

from events.models import Assignment


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = "__all__"
        exclude = ["manager", "status"]
        labels = {"name": "Name", "event_date": "Deadline", "employee": "Assigned Employees"}


class AssignmentStatusForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ["status"]
