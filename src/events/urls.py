from django.urls import path

from events.views import (AssignmentCreateView, AssignmentListView,
                          CalendarDetailView)

urlpatterns = [
    path('<int:year>/<str:month>', CalendarDetailView.as_view(), name='calendar'),
    path('assignments/', AssignmentListView.as_view(), name='assignments'),
    path('assignments/create', AssignmentCreateView.as_view(), name='assignments-create')
]

