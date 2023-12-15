from django.urls import path

from events.views import (
    AssignmentCloseView,
    AssignmentCreateView,
    AssignmentListView,
    CalendarDetailView,
)

urlpatterns = [
    path("<int:year>/<int:month_number>", CalendarDetailView.as_view(), name="calendar"),
    path("assignments/", AssignmentListView.as_view(), name="assignments"),
    path("assignments/create", AssignmentCreateView.as_view(), name="assignments-create"),
    path("assignments/<int:pk>/close", AssignmentCloseView.as_view(), name="assignments-close"),
]
