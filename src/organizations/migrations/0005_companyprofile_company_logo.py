# Generated by Django 5.0.1 on 2024-01-29 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0004_alter_companyprofile_company"),
    ]

    operations = [
        migrations.AddField(
            model_name="companyprofile",
            name="company_logo",
            field=models.ImageField(
                default="media/organizations/company_logo/default.jpg", upload_to="media/organizations/company_logo"
            ),
        ),
    ]