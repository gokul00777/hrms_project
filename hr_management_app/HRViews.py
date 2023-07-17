from datetime import datetime
from uuid import uuid4
from django.http import Http404
from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from hr_management_app.models import Employees, LeaveReportHR,\
        HRs, FeedBackHRs, CustomUser, NotificationHRs
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.decorators import login_required
from .views import doLogin
from .decorators import require_user_type


@login_required(login_url=doLogin)
@require_user_type(2)
def hr_home(request):
    employee_count=Employees.objects.filter(admin=request.user.id).count()
    leave_count = LeaveReportHR.objects.filter(hr_id=request.user.id, leave_status=1).count()


    employee_attendance=Employees.objects.filter()
    employee_list=[]
    employee_list_attendance_present=[]
    employee_list_attendance_absent=[]
    for employee in employee_attendance:
        # attendance_present_count=AttendanceReport.objects.filter(status=True,employee_id=employee.id).count()
        # attendance_absent_count=AttendanceReport.objects.filter(status=False,employee_id=employee.id).count()
        employee_list.append(employee.admin.username)
        # employee_list_attendance_present.append(attendance_present_count)
        # employee_list_attendance_absent.append(attendance_absent_count)

    return render(request,"hr_management/hr/hr_home_template.html",{"employee_count":employee_count,"leave_count":leave_count,"employee_list":employee_list,"present_list":employee_list_attendance_present,"absent_list":employee_list_attendance_absent})




@login_required(login_url=doLogin)
@require_user_type(2)
def hr_apply_leave(request):
    try:
        hr_object = HRs.objects.get(admin=request.user)
    except ObjectDoesNotExist as e:
        logger.error(f"Could not find HRs object for user {request.user}: {str(e)}")
        return redirect("show_login")  # or render a custom error page

    leave_data = LeaveReportHR.objects.filter(hr_id=hr_object)
    return render(request, "hr_management/hr/hr_apply_leave.html", {"leave_data": leave_data})


@login_required(login_url=doLogin)
@require_user_type(2)
def hr_apply_leave_save(request):
    if request.method == "POST":
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")
        hr_object = HRs.objects.get(admin=request.user)

        leave_report = LeaveReportHR()
        leave_report.leave_date = leave_date
        leave_report.leave_message = leave_msg
        leave_report.hr_id = hr_object  # add the hr_id field
        leave_report.save()

        messages.success(request, "Leave applied successfully!")
        return redirect("hr_apply_leave")
    else:
        return render(request, "hr_management/hr/hr_apply_leave.html")




@login_required(login_url=doLogin)
@require_user_type(2)
def hr_feedback(request):
    hr_id=HRs.objects.get(admin=request.user.id)
    feedback_data=FeedBackHRs.objects.filter(hr_id=hr_id)
    return render(request,"hr_management/hr/hr_feedback.html",{"feedback_data":feedback_data})


@login_required(login_url=doLogin)
@require_user_type(2)
def hr_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("hr_feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        hr_obj=HRs.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackHRs(hr_id=hr_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(("hr_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(("hr_feedback"))

@login_required(login_url=doLogin)
@require_user_type(2)
def hr_profile(request):
    try:
        user=CustomUser.objects.get(id=request.user.id)
        hr=HRs.objects.get(admin=user)
        return render(request,"hr_management/hr/hr_profile.html",{"user":user,"hr":hr})
    except CustomUser.DoesNotExist:
        raise Http404("CustomUser matching query does not exist")
    except HRs.DoesNotExist:
        raise Http404('HR matching query does not exist')


@login_required(login_url=doLogin)
@require_user_type(2)
def hr_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("hr_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            hr=HRs.objects.get(admin=customuser.id)
            hr.address=address
            hr.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("hr_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("hr_profile"))


@login_required(login_url=doLogin)
@require_user_type(2)
@csrf_exempt
def hr_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        hr=HRs.objects.get(admin=request.user.id)
        hr.fcm_token=token
        hr.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@login_required(login_url=doLogin)
@require_user_type(2)
def hr_all_notification(request):
    hr=HRs.objects.get(admin=request.user.id)
    notifications=NotificationHRs.objects.filter(hr_id=hr.id)
    return render(request,"hr_management/hr/all_notification.html",{"notifications":notifications})

