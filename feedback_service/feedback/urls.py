from django.urls import path
from .views import FeedbackProcessView, FeedbackResultView

urlpatterns = [
    path('process/', FeedbackProcessView.as_view(), name='feedback-process'),
    path('results/<str:task_id>/', FeedbackResultView.as_view(), name='feedback-results'),
]
