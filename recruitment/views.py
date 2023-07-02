# from django.shortcuts import render
# from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
# from django.contrib.auth.mixins import PermissionRequiredMixin
# from .models import JobOffer, JobApplication
#
#
# class CandidateDefaultView(View):
#     template_name = "recruitment/candidate.html"
#
#     def get(self, request):
#         context = {"title": "Candidate"}
#         return render(request, self.template_name, context)
#
#
# class JobOffersView(ListView):
#     model = JobOffer
#     template_name = "recruitment/job_offers.html"
#     context_object_name = "job_offers"
#     ordering = ["-status", "-published_date"]
#     paginate_by = 5
#
#
# class JobOfferView(DetailView):
#     model = JobOffer
#     template_name = "recruitment/job_offer_detail.html"
#     context_object_name = "job_offer"
#
#
# class JobOfferUpdate(PermissionRequiredMixin, UpdateView):
#     permission_required = "recruitment.change_joboffer"
#
#     model = JobOffer
#     template_name = "recruitment/job_offer_update.html"
#     context_object_name = "job_offer"
#     fields = "__all__"
#
#
# class JobOfferCreate(PermissionRequiredMixin, CreateView):
#     permission_required = "recruitment.add_joboffer"
#
#     model = JobOffer
#     template_name = "recruitment/job_offer_update.html"
#     context_object_name = "job_offer"
#     fields = "__all__"
#
#
# class ApplyJobOffer(CreateView):
#     model = JobApplication
#     template_name = "recruitment/job_application.html"
#     context_object_name = "job_application"
#     fields = "__all__"
#
#     def form_valid(self, form):
#         # if not request.user.is_anonymous:
#         # if self.request.user.is_authenticated:
#         #     form.instance.candidate = self.request.user
#         try:
#             form.instance.candidate = self.request.user
#         except ValueError as e:
#             pass
#             # print(f'User creation failed reason {e}')
#         return super().form_valid(form)
