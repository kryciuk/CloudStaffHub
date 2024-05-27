from django.shortcuts import reverse
from django.test import TransactionTestCase
from rest_framework import status

from users.factories import EmployeeFactory, OwnerFactory


class TestQuestionnaireCreateView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner1 = OwnerFactory()
        self.user_employee = EmployeeFactory()
        self.user_employee.profile.company = self.user_owner1.profile.company
        self.user_employee.profile.save()

    def test_owner_can_access_questionnaire_create(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("questionnaire-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_employee_cant_access_questionnaire_create(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("questionnaire-create"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    # def test_owner_can_change_own_company_info_and_industry(self):
    #     self.client.force_login(self.user_owner1)
    #     industry = Industry.objects.get(id=1)
    #     response = self.client.post(
    #         reverse("company-profile", kwargs={"pk": self.user_owner1.profile.company.id}),
    #         data={"info": "updated company info", "industries": industry.id},
    #         follow=True,
    #     )
    #     company1_profile = CompanyProfile.objects.get(id=self.user_owner1.profile.company.id)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(company1_profile.info, "updated company info")
    #     self.assertEqual(len(company1_profile.industries.all()), 1)
    #
    # def test_owner_can_change_own_company_industries_many_at_once(self):
    #     self.client.force_login(self.user_owner1)
    #     industries_start_with_a = Industry.objects.filter(industry__startswith="A")
    #     response = self.client.post(
    #         reverse("company-profile", kwargs={"pk": self.user_owner1.profile.company.id}),
    #         data={"info": "updated company info", "industries": [industry.id for industry in industries_start_with_a]},
    #         follow=True,
    #     )
    #     company1_profile = CompanyProfile.objects.get(id=self.user_owner1.profile.company.id)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(company1_profile.info, "updated company info")
    #     self.assertEqual(len(company1_profile.industries.all()), 4)
    #
    # def test_owner_cant_change_other_company_info_and_industry(self):
    #     self.client.force_login(self.user_owner2)
    #     industry = Industry.objects.get(id=1)
    #     response = self.client.post(
    #         reverse("company-profile", kwargs={"pk": self.user_owner1.profile.company.id}),
    #         data={"info": "updated company info", "industries": industry.id},
    #         follow=True,
    #     )
    #     company1_profile = CompanyProfile.objects.get(id=self.user_owner1.profile.company.id)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(company1_profile.info, None)
    #
    # def test_employee_cant_access_is_redirected(self):
    #     self.client.force_login(self.user_employee)
    #     response = self.client.get(reverse("company-profile", kwargs={"pk": self.user_employee.profile.company.id}))
    #     self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    #
    # def test_if_title_if_correct(self):
    #     self.client.force_login(self.user_owner1)
    #     response = self.client.get(reverse("company-profile", kwargs={"pk": self.user_employee.profile.company.id}))
    #     title = response.context["title"]
    #     self.assertEqual(title, f"{self.user_owner1.profile.company.name} Profile - CloudStaffHub")
    #
    # def test_if_correct_template_used(self):
    #     self.client.force_login(self.user_owner1)
    #     response = self.client.get(reverse("company-profile", kwargs={"pk": self.user_employee.profile.company.id}))
    #     self.assertTemplateUsed(response, "organizations/company_profile.html")
    #
