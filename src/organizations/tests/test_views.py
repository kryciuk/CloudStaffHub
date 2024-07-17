from django.shortcuts import reverse
from django.test import TransactionTestCase
from rest_framework import status

from organizations.models import Company, CompanyProfile, Industry
from users.factories import EmployeeFactory, OwnerFactory


class TestCompanyProfileView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user_owner1 = OwnerFactory()
        self.user_owner2 = OwnerFactory()
        self.user_employee = EmployeeFactory()
        self.user_employee.profile.company = self.user_owner1.profile.company
        self.user_employee.profile.save()

    def test_owner_can_access_own_company_profile(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("company-profile", kwargs={"pk": self.user_owner1.profile.company.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_cant_access_other_company_profile(self):
        self.client.force_login(self.user_owner2)
        response = self.client.get(reverse("company-profile", kwargs={"pk": self.user_owner1.profile.company.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_change_own_company_info_and_industry(self):
        self.client.force_login(self.user_owner1)
        industry = Industry.objects.get(id=1)
        response = self.client.post(
            reverse("company-profile", kwargs={"pk": self.user_owner1.profile.company.id}),
            data={"info": "updated company info", "industries": industry.id},
            follow=True,
        )
        company1_profile = CompanyProfile.objects.get(id=self.user_owner1.profile.company.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(company1_profile.info, "updated company info")
        self.assertEqual(len(company1_profile.industries.all()), 1)

    def test_owner_can_change_own_company_industries_many_at_once(self):
        self.client.force_login(self.user_owner1)
        industries_start_with_a = Industry.objects.filter(industry__startswith="A")
        response = self.client.post(
            reverse("company-profile", kwargs={"pk": self.user_owner1.profile.company.id}),
            data={"info": "updated company info", "industries": [industry.id for industry in industries_start_with_a]},
            follow=True,
        )
        company1_profile = CompanyProfile.objects.get(id=self.user_owner1.profile.company.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(company1_profile.info, "updated company info")
        self.assertEqual(len(company1_profile.industries.all()), 4)

    def test_owner_cant_change_other_company_info_and_industry(self):
        self.client.force_login(self.user_owner2)
        industry = Industry.objects.get(id=1)
        response = self.client.post(
            reverse("company-profile", kwargs={"pk": self.user_owner1.profile.company.id}),
            data={"info": "updated company info", "industries": industry.id},
            follow=True,
        )
        company1_profile = CompanyProfile.objects.get(id=self.user_owner1.profile.company.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(company1_profile.info, None)

    def test_employee_cant_access_is_redirected(self):
        self.client.force_login(self.user_employee)
        response = self.client.get(reverse("company-profile", kwargs={"pk": self.user_employee.profile.company.id}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_if_title_is_correct(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("company-profile", kwargs={"pk": self.user_employee.profile.company.id}))
        title = response.context["title"]
        self.assertEqual(title, f"{self.user_owner1.profile.company.name} Profile - CloudStaffHub")

    def test_if_correct_template_used(self):
        self.client.force_login(self.user_owner1)
        response = self.client.get(reverse("company-profile", kwargs={"pk": self.user_employee.profile.company.id}))
        self.assertTemplateUsed(response, "organizations/company_profile.html")


class TestCompanyRegisterView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.data = {
            "company-name": "ABC",
            "company-email_domain": "abc.com",
            "user-username": "BossABC",
            "user-first_name": "Ann",
            "user-last_name": "Smith",
            "user-email": "bossabc@abc.com",
            "user-password1": "Miksery1!",
            "user-password2": "Miksery1!",
        }

    def test_new_company_can_be_registered_and_message_shown(self):
        response = self.client.post(reverse("register-company"), data=self.data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, f"Company {self.data.get('company-name')} was registered successfully.")

    def test_new_company_is_not_registered_if_wrong_data(self):
        self.data["user-email"] = "bossabc@aaa.com"
        response = self.client.post(reverse("register-company"), self.data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Company.objects.all()), 0)
        self.assertContains(response, "User and company domains do not match.")

    def test_new_company_is_not_registered_if_exists_in_database(self):
        self.user_owner1 = OwnerFactory()
        self.data.update(
            {
                "company-name": self.user_owner1.profile.company,
                "company-email_domain": self.user_owner1.profile.company.email_domain,
            }
        )
        response = self.client.post(reverse("register-company"), data=self.data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Company.objects.all()), 1)
        self.assertContains(response, "Company with this name already exists.")

    def test_if_title_is_correct(self):
        response = self.client.get(reverse("register-company"))
        title = response.context["title"]
        self.assertEqual(title, "Register Company - Cloud Staff Hub")

    def test_if_correct_template_used(self):
        response = self.client.get(reverse("register-company"))
        self.assertTemplateUsed(response, "organizations/register_company.html")
