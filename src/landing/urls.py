from django.urls import path

from landing.views.index import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
