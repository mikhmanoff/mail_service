# mail/views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from .serializers import EmailSerializer
import os
from dotenv import load_dotenv

load_dotenv()

class SendEmailApiView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            to_email = serializer.validated_data['to_email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            
            send_mail(
                subject,
                message,
                os.getenv('EMAIL_HOST_USER'),  # From email
                [to_email],
                fail_silently=False,
            )
            return Response({'status': 'Email sent successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendEmailFormView(View):
    def get(self, request):
        return render(request, 'send_email.html')

    def post(self, request):
        to_email = request.POST.get('to_email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        try:
            send_mail(
                subject,
                message,
                os.getenv('EMAIL_HOST_USER'),  # From email
                [to_email],
                fail_silently=False,
            )
            messages.success(request, 'Email sent successfully!')
        except Exception as e:
            messages.error(request, f'Error sending email: {str(e)}')
        
        return redirect('send-email-form')
