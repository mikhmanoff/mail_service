from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import fetch_emails

class SendEmailView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            to_email = serializer.validated_data['to_email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            
            send_mail(
                subject,
                message,
                'your_email@gmail.com',  # From email
                [to_email],
                fail_silently=False,
            )
            return Response({'status': 'Email sent successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FetchEmailView(APIView):
    def get(self, request):
        emails = fetch_emails()
        return Response(emails, status=status.HTTP_200_OK)