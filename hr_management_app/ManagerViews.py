from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .decorators import require_user_type
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .decorators import require_user_type


@require_user_type(user_type=4)
@login_required(login_url='do_login')
def manager_home(request):
    return render(request,"hr_management/manager_template/manager_home_template.html")


@require_user_type(user_type=4)


@require_user_type(user_type=4)
@login_required(login_url='do_login')
def manager_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    # manager=Managers.objects.get(admin=user)
    return render(request,"hr_management/manager_template/manager_profile.html",{"user":user})


@require_user_type(user_type=4)
@login_required(login_url='do_login')
def manager_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manager_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        profile_pic=request.POST.get("profile_pic")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("manager_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("manager_profile"))


@login_required(login_url='do_login')
@require_user_type(user_type=[1, 4])
def manager_leave_view(request):
    user = request.user
    if user.user_type == '4':
        manager_id = user.id
        # Retrieve the manager instance from CustomUser model
        manager = CustomUser.objects.get(id=manager_id, user_type='4')
        # Get the employees managed by the manager
        customusers = CustomUser.objects.filter(manager=manager)

        context = {
            'leaves': [],
            'current_time': datetime.now()
        }

        for customuser in customusers:
            customuser_ids = []
            leave_reports = []

            customuser_ids.append(customuser.id)

            employees = Employees.objects.filter(admin_id__in=customuser_ids)

            for employee in employees:
                l = LeaveReportEmployee.objects.filter(employee_id_id=employee)
                leave_reports.extend(l)

            context['leaves'].extend(leave_reports)

        return render(request, "hr_management/manager_template/employee_leave_view.html", context)
