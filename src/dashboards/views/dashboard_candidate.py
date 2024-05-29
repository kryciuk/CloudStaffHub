import random
from random import randrange

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.generic import TemplateView

from organizations.models import Company, Industry
from recruitment.models import JobOffer


class CandidateDashboardView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "dashboards/dashboard_candidate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # random company

        context["random_company"] = None
        if len(Company.objects.all()) != 0:
            random_company = randrange(1, len(Company.objects.all()) + 1)
            context["random_company"] = Company.objects.get(id=random_company)

        # job offers tailored to user

        user_interested_in_field = self.request.user.profile.interested_in
        user_interested_in_department = self.request.user.profile.department

        proposed_job_offers = JobOffer.objects.filter(status=True).order_by("-id")[:5]

        if user_interested_in_department is not None and user_interested_in_field is not None:
            proposed_job_offers = JobOffer.objects.filter(
                company__companyprofile__industries=user_interested_in_field,
                position__department__name=user_interested_in_department.name,
                status=True,
            ).order_by("-id")[:5]
        proposed_job_offers_by_department = (
            JobOffer.objects.filter(position__department__name=user_interested_in_department, status=True)
            .exclude(company__companyprofile__industries=user_interested_in_field)
            .order_by("-id")[:5]
        )
        if user_interested_in_department is not None:
            proposed_job_offers_by_field = (
                JobOffer.objects.filter(company__companyprofile__industries=user_interested_in_field, status=True)
                .exclude(position__department__name=user_interested_in_department.name)
                .order_by("-id")[:5]
            )
        else:
            proposed_job_offers_by_field = (
                JobOffer.objects.filter(company__companyprofile__industries=user_interested_in_field, status=True)
                .exclude(id__in=proposed_job_offers)
                .order_by("-id")[:5]
            )
        newest_entries_not_personalized = JobOffer.objects.filter(status=True).order_by("-id")[:5]

        context["newest_entries"] = proposed_job_offers
        context["newest_entries_department"] = proposed_job_offers_by_department
        context["newest_entries_field"] = proposed_job_offers_by_field
        context["newest_entries_not_personalized"] = newest_entries_not_personalized

        # articles tips job hunting

        results_tips = requests.get(
            "https://newsapi.org/v2/everything?q=job+hunting+tips&apiKey=063c8ff3b9ab476297774505a481006d", timeout=5
        ).json()
        context["article_tips"] = "Currently there are no articles..."
        if results_tips["status"] != "error":
            articles_tips = results_tips["articles"]
            random_article_tips = random.randrange(0, len(articles_tips))
            article_tips = articles_tips[random_article_tips]
            context["article_tips"] = article_tips

        # articles interested in

        yesterday = timezone.datetime.now() - timezone.timedelta(days=2)
        oldest_article_date = yesterday.strftime("%Y-%m-%d")

        try:
            industry = user_interested_in_field.industry
        except AttributeError:
            industries = list(Industry.objects.all())
            random_industry = random.choice(industries)
            industry = random_industry.industry

        context["industry"] = industry
        results_industry = requests.get(
            f"https://newsapi.org/v2/everything?q={industry}&sortby=relevancy&language=en&from={oldest_article_date}&apiKey=063c8ff3b9ab476297774505a481006d",
            timeout=5,
        ).json()
        context["article_industry"] = "Currently there are no articles..."
        if results_industry["status"] != "error":
            articles_industry = results_industry["articles"]
            most_relevant = round(len(articles_industry) * 0.3)
            random_article_industry = random.randrange(0, most_relevant)
            article_industry = articles_industry[random_article_industry]
            context["article_industry"] = article_industry

        context["title"] = "Candidate's Dashboard - CloudStaffHub"

        return context
