import datetime
import json
import os
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from hr_management_app.EmailBackEnd import EmailBackEnd
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from django.db.models import Q


def ShowLoginPage(request):
    return render(request,"hr_management/login_page.html")

def doLogin(request):
        captcha_token=request.POST.get("g-recaptcha-response")
        cap_url="https://www.google.com/recaptcha/api/siteverify"
        cap_secret="6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
        cap_data={"secret":cap_secret,"response":captcha_token}
        cap_server_response=requests.post(url=cap_url,data=cap_data)
        cap_json=json.loads(cap_server_response.text)

        if cap_json['success']==False:
            messages.error(request,"Invalid Captcha Try Again")
            return HttpResponseRedirect("/")
    

        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect(("/hr_home"))
            elif user.user_type=="3":
                return HttpResponseRedirect(("/employee_home"))
            elif user.user_type=="4":
                return HttpResponseRedirect(("/manager_home"))
            else:
                return HttpResponse('ddddddddddd')
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "YOUR_API_KEY",' \
         '        authDomain: "FIREBASE_AUTH_URL",' \
         '        databaseURL: "FIREBASE_DATABASE_URL",' \
         '        projectId: "FIREBASE_PROJECT_ID",' \
         '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
         '        messagingSenderId: "FIREBASE_SENDER_ID",' \
         '        appId: "FIREBASE_APP_ID",' \
         '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")


def signup_admin(request):
    return render(request,"hr_management/signup_admin_page.html")


def signup_employee(request):
    employee=Employees.objects.all()
    return render(request,"hr_management/signup_employee_page.html",{"employee":employee})


def signup_hr(request):
    return render(request,"hr_management/signup_hr_page.html")

def signup_manager(request):
    return render(request,"hr_management/signup_manager_page.html")


def do_admin_signup(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")


    try:
        user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email,user_type=1)
        user.save()
        messages.success(request,"Successfully Created Admin")
        return HttpResponseRedirect(reverse("show_login"))
    except BaseException as a:
        print(a)
        messages.error(request,"Failed to Create Admin")
        return HttpResponseRedirect(reverse("show_login"))

def do_hr_signup(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    try:
        user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email,user_type=2)
        user.save()
        messages.success(request,"Successfully Created HR")
        return HttpResponseRedirect(reverse("show_login"))
    except BaseException as e:
        print(e)
        messages.error(request,"Failed to Create HR")
        return HttpResponseRedirect(reverse("show_login"))


def do_signup_employee(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    # Check if an employee with the same username or email already exists
    if CustomUser.objects.filter(Q(username=username) | Q(email=email)).exists():
        messages.error(request, "An employee with the same username or email already exists.")
        return HttpResponseRedirect(reverse("show_login"))

    try:
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            last_name=last_name,
            first_name=first_name,
            user_type=3
        )
        user.employees.save()

        messages.success(request, "Successfully added employee.")
        return HttpResponseRedirect(reverse("show_login"))
    except BaseException as e:
        messages.error(request, f"Failed to create employee: {str(e)}")
        return HttpResponseRedirect(reverse("show_login"))


    
def do_signup_manager(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    # Check if an employee with the same username or email already exists
    if CustomUser.objects.filter(Q(username=username) | Q(email=email)).exists():
        messages.error(request, "An manager with the same username or email already exists.")
        return HttpResponseRedirect(reverse("show_login"))

    try:
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            last_name=last_name,
            first_name=first_name,
            user_type=4
        )
        user.employees.save()
        messages.success(request, "Successfully added employee.")
        return HttpResponseRedirect(reverse("show_login"))
    except BaseException as e:
        messages.error(request, f"Failed to create manager: {str(e)}")
        return HttpResponseRedirect(reverse("show_login"))




















from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from hr_management_app.models import CustomUser
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'No user with the provided email address exists.')
            return redirect('reset_password')

        # Generate the password reset token
        token = default_token_generator.make_token(user)

        # Generate the password reset link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri('/password_reset/{}/{}/'.format(uid, token))

        # Compose the email
        subject = 'Password Reset'
        message = render_to_string('hr_management/reset_password_email.html', {
            'user': user,
            'reset_link': reset_link
        })
        email = EmailMessage(subject, message, to=[email])
        email.send()

        messages.success(request, 'Password reset email has been sent. Please check your inbox.')
        return redirect('reset_password')

    return render(request, 'hr_management/reset_password.html')
