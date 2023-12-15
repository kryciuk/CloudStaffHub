from django.forms import ModelForm

from organizations.models import Department


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['name']
