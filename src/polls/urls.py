from django.urls import path

from polls.views import (PollAnswerView, PollCloseView, PollCreateView,
                         PollFillView, PollListView, PollResultsView,
                         PollUpdateView)

urlpatterns = [path("create", PollCreateView.as_view(), name="poll-create"),
               path("<int:pk>/fill", PollFillView.as_view(), name="poll-fill"),
               path("list", PollListView.as_view(), name="poll-list"),
               path("<int:pk>/detail", PollUpdateView.as_view(), name="poll-update"),
               path("<int:pk>/close", PollCloseView.as_view(), name="poll-close"),
               path("<int:pk>/answer", PollAnswerView.as_view(), name="poll-answer"),
               path("<int:pk>/results", PollResultsView.as_view(), name="poll-results")]
