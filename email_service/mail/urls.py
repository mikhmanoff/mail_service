# mail/urls.py
from django.urls import path
from .views import SendEmailApiView, SendEmailFormView, FetchEmailsView

urlpatterns = [
    path('send-email-api/', SendEmailApiView.as_view(), name='send-email-api'),
    path('send-email-form/', SendEmailFormView.as_view(), name='send-email-form'),
    path('fetch-emails/', FetchEmailsView.as_view(), name='fetch-emails'),
]
