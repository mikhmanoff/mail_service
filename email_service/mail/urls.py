from django.urls import path
from .views import SendEmailView, FetchEmailView

urlpatterns = [
    path('send-email/', SendEmailView.as_view(), name='send-email'),
    path('fetch-emails/', FetchEmailView.as_view(), name='fetch-emails'),
]