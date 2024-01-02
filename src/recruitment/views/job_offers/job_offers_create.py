from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import CreateView

from organizations.models import City
from recruitment.forms import JobOfferForm
from recruitment.models import Position


class JobOffersCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = "recruitment.add_joboffer"
    form_class = JobOfferForm
    template_name = "recruitment/job_offers/job_offer_update.html"
    context_object_name = "job_offer"

    def get_form(self, form_class=JobOfferForm):
        form = super().get_form()
        form.fields["expiry_date"].widget = DateTimePickerInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"].fields["position"].queryset = Position.objects.filter(
            company=self.request.user.profile.company
        )
        context["title"] = "Job Offer Create - CloudStaffHub"
        return context

    def form_valid(self, form):
        form.instance.company = self.request.user.profile.company
        form.instance.published_date = timezone.datetime.now()
        form.instance.status = True
        messages.success(self.request, "Job offer was created successfully.")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        request.session["previous_view"] = "JobOffersCreateView"
        return super().get(request, *args, **kwargs)


def load_cities(request):
    country = request.GET.get("country")
    cities = City.objects.filter(country=country).order_by("name")
    return JsonResponse(list(cities.values("id", "name")), safe=False)
