from django.urls import path
from polls.views import PollCreateView, PollFillView, PollListView, PollUpdateView, PollCloseView, PollAnswerCreateView

urlpatterns = [path("create", PollCreateView.as_view(), name="poll-create"),
               path("<int:pk>/fill", PollFillView.as_view(), name="poll-fill"),
               path("list", PollListView.as_view(), name="poll-list"),
               path("<int:pk>/detail", PollUpdateView.as_view(), name="poll-update"),
               path("<int:pk>/close", PollCloseView.as_view(), name="poll-close"),
               path("<int:pk>/answer", PollAnswerCreateView.as_view(), name="poll-answer-create")]