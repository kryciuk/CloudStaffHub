from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("landing.urls")),
    path("user/", include("users.urls")),
    path("recruitment/", include("recruitment.urls")),
    path("evaluation/", include("evaluation.urls")),
    path("recruiter/", include("recruiter.urls")),
    path("organizations/", include("organizations.urls")),
    path("dashboard/", include("dashboards.urls")),
    path("polls/", include("polls.urls")),
    path("calendar/", include("events.urls")),
    path("company-owner/", include("owner.urls")),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon/favicon.ico"))),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL) + [path("silk/", include("silk.urls", namespace="silk"))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
