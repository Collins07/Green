from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
import smtplib
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.conf import settings
from .utils import account_activation_token

from django.contrib import auth
import threading


# Create your views here




class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username is already taken, try another one'}, status=409)
        
        return JsonResponse({'username_valid': True})
    

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry! email is already in use'}, status=409)
        
        return JsonResponse({'email_valid': True})    



class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # get user data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValue': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()

                auth.login(request, user)  # Log in the user

                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')  # Redirect to the login page

        return render(request, 'authentication/register.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    # Redirect to the home page or any other desired page
                    return redirect('home')
                else:
                    messages.error(request, 'Your account is not active. Please check your email.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill in all fields.')

        return render(request, 'authentication/login.html')



class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        return redirect ('home')