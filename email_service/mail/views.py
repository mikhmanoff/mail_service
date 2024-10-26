# mail/views.py
import imaplib
import email
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from .serializers import EmailSerializer
import os
from dotenv import load_dotenv
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


load_dotenv()

class SendEmailApiView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            to_email = serializer.validated_data['to_email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            
            email = EmailMultiAlternatives(
                subject=subject,
                body='This is the plain text version of the email',  # Add a plain text fallback version
                from_email=os.getenv('EMAIL_HOST_USER'),
                to=[to_email],
            )
            email.attach_alternative(message, "text/html")
            email.send()

            return Response({'status': 'Email sent successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendEmailFormView(View):
    def get(self, request, *args, **kwargs):
        # Обработка GET-запроса для отображения формы
        return render(request, 'send_email.html')

    def post(self, request, *args, **kwargs):
        to_email = request.POST.get('to_email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')  # Это уже HTML-содержимое

        try:
            # Создание email с HTML и plain text версиями
            email = EmailMultiAlternatives(
                subject=subject,
                body=strip_tags(message),  # Текстовая версия (без HTML)
                from_email=os.getenv('EMAIL_HOST_USER'),
                to=[to_email]
            )
            email.attach_alternative(message, "text/html")  # HTML-версия
            email.send()

            messages.success(request, 'Email sent successfully!')
        except Exception as e:
            messages.error(request, f'Error sending email: {str(e)}')

        return redirect('send-email-form')

class FetchEmailsView(View):
    def get(self, request):
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(os.getenv('EMAIL_HOST_USER'), os.getenv('EMAIL_HOST_PASSWORD'))
            mail.select('inbox')

            status, messages_list = mail.search(None, 'ALL')
            email_ids = messages_list[0].split()

            emails = []
            for e_id in email_ids[-5:]:  # Fetch the last 5 emails
                status, msg_data = mail.fetch(e_id, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg['subject']
                        from_ = msg['from']
                        try:
                            body = msg.get_payload(decode=True).decode()
                        except AttributeError:
                            body = "No content"
                        emails.append({'from': from_, 'subject': subject, 'body': body})

            mail.logout()
        except Exception as e:
            messages.error(request, f'Error fetching emails: {str(e)}')
            emails = []

        return render(request, 'incoming_emails.html', {'emails': emails})
