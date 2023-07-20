import json
import requests
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from .models import *
from django.conf import settings
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from num2words import num2words
import datetime
from django.utils.html import strip_tags
from django.db.models import Q
from datetime import datetime
from .decorators import require_user_type
from django.contrib import messages
from decimal import Decimal
from django.http import HttpResponse
from io import BytesIO
from django.core.mail import EmailMessage
from datetime import date
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from num2words import num2words
from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from .models import Employee_Onboarding, BankDetails, SalarySlip
from django.db.models import Q





@login_required(login_url='do_login')
@require_user_type(1)
def admin_home(request):
    employee_count1=Employees.objects.all().count()
    hr_count=HRs.objects.all().count()

    hrs=HRs.objects.all()
    attendance_present_list_hr=[]
    attendance_absent_list_hr=[]
    hr_name_list=[]
    for hr in hrs:
        leaves=LeaveReportHR.objects.filter(hr_id=hr.id,leave_status=1).count()
        hr_name_list.append(hr.admin.username)

    employees_all=Employees.objects.all()
    attendance_present_list_employee=[]
    attendance_absent_list_employee=[]
    employee_name_list=[]
    for employee in employees_all:
        leaves=LeaveReportEmployee.objects.filter(employee_id=employee.id,leave_status=1).count()
        employee_name_list.append(employee.admin.username)
    return render(request,"hr_management/admin/home_content.html",{"employee_count":employee_count1,"hr_count":hr_count,"hr_name_list":hr_name_list,"attendance_present_list_hr":attendance_present_list_hr,"attendance_absent_list_hr":attendance_absent_list_hr,"employee_name_list":employee_name_list,"attendance_present_list_employee":attendance_present_list_employee,"attendance_absent_list_employee":attendance_absent_list_employee})


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_hr(request):
    manager = CustomUser.objects.filter(user_type=4)
    if request.user.user_type =='2': 
        return render(request,"hr_management/hr/add_hr_template.html")
    else:
        return render(request,"hr_management/admin/add_hr_template.html",{"manager":manager})
      

@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_hr_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        department=request.POST.get("department")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.hrs.department=department
            user.save()

            # Send email notification
            email_subject = 'HR Account Created'
            application_link = 'http://127.0.0.1:8000' 
            email_template = 'hr_management/admin/hr_account_created.html'  # Path to your email template
            email_context =  {'first_name': first_name, 'last_name': last_name,'email':email,'password':password,'application_link':application_link}  # Context data for the template


            
            # Render the HTML email template and convert it to a plain text version
            email_html_message = render_to_string(email_template, email_context)
            email_plain_message = strip_tags(email_html_message)
            # Set up the email parameters
            from_email = getattr(settings, 'EMAIL_HOST_USER', 'default_from_email')
            to_email = email

            # Create the EmailMessage object
            email_message = EmailMessage(
                subject=email_subject,
                body=email_plain_message,
                from_email=from_email,
                to=[to_email]
            )
            email_message.send()

            messages.success(request,"Successfully Added HR")
            return HttpResponseRedirect(reverse("add_hr"))
        except:
            messages.error(request,"Failed to Add HR")
            return HttpResponseRedirect(reverse("add_hr"))

@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_employee(request):
    manager = CustomUser.objects.filter(user_type=4)
    if request.user.user_type =='2': 
        return render(request,"hr_management/hr/add_employee_template.html",{"manager":manager})
    else:
        return render(request,"hr_management/admin/add_employee_template.html",{"manager":manager})
      


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_employee_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        manager = request.POST.get("manager")
        department = request.POST.get("department")
        designation = request.POST.get("designation")

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name, first_name=first_name, manager=manager, user_type=3)
            user.employees.department = department
            user.employees.designation = designation
            user.save()

            # Send email notification
            email_subject = 'Employee Account Created'
            application_link = 'http://127.0.0.1:8000' 
            email_template = 'hr_management/admin/employee_account_created.html'  # Path to your email template
            email_context =  {'first_name': first_name, 'last_name': last_name,'email':email,'password':password,'application_link':application_link}  # Context data for the template


            
            # Render the HTML email template and convert it to a plain text version
            email_html_message = render_to_string(email_template, email_context)
            email_plain_message = strip_tags(email_html_message)
            # Set up the email parameters
            from_email = getattr(settings, 'EMAIL_HOST_USER', 'default_from_email')
            to_email = email

            # Create the EmailMessage object
            email_message = EmailMessage(
                subject=email_subject,
                body=email_plain_message,
                from_email=from_email,
                to=[to_email]
            )
            email_message.send()

            messages.success(request, "Successfully added employee and sent email notification")
            return HttpResponseRedirect(reverse("add_employee"))
        except:
            messages.error(request, "Failed to add employee")
            return HttpResponseRedirect(reverse("add_employee"))
    

@login_required(login_url='do_login')
@require_user_type(user_type=[1, 2])
def manage_hr(request):
    hrs = HRs.objects.all()
    if request.user.user_type == '2':
        return render(request, "hr_management/hr/manage_hr_template.html", {"hrs": hrs})
    else:
        return render(request, "hr_management/admin/manage_hr_template.html", {"hrs": hrs})
    
@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def manage_employee(request):
    query = request.GET.get('search')
    if query:
        if query.isdigit(): # check if query is a number
            employees = Employees.objects.filter(Q(admin__email__icontains=query) | Q(admin__id=query) | Q(admin__first_name=query) | Q(admin__last_name=query))
            hrs = HRs.objects.filter(Q(admin__email__icontains=query) | Q(admin__id=query) | Q(admin__first_name=query) | Q(admin__last_name=query))
        else:
            employees = Employees.objects.filter(Q(admin__email__icontains=query) | Q(admin__first_name=query) | Q(admin__last_name=query))
            hrs = HRs.objects.filter(Q(admin__email__icontains=query) | Q(admin__id=query) | Q(admin__first_name=query) | Q(admin__last_name=query))
    else:
        employees = Employees.objects.all()   
        hrs = HRs.objects.all()    

    if request.user.user_type == '2':
        return render(request, "hr_management/hr/manage_employee_template.html", {"employees": employees,'hrs':hrs})
    else:
        return render(request, "hr_management/admin/manage_employee_template.html", {"employees": employees,'hrs':hrs})


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_manager(request):
    try:
        manager = CustomUser.objects.filter(Q(user_type=4) | Q(user_type=1))
        if request.user.user_type =='2': 
            return render(request,"hr_management/hr/add_manager_template.html",{"manager":manager})
        else:
            return render(request,"hr_management/admin/add_manager_template.html",{"manager":manager})
    except:
        messages.error(request,"Failed to Add Manager")
        return HttpResponseRedirect(reverse("add_manager"))



@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_manager_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        manager=request.POST.get("manager")
        department=request.POST.get("department")
        designation=request.POST.get("designation")

        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,manager=manager,user_type=4)
            user.employees.department=department
            user.employees.designation=designation
            user.save()
            
            # Send email notification
            email_subject = 'Manager Account Created'
            application_link = 'http://127.0.0.1:8000' 
            email_template = 'hr_management/admin/manager_account_created.html'  # Path to your email template
            email_context =  {'first_name': first_name, 'last_name': last_name,'email':email,'password':password,'application_link':application_link}  # Context data for the template


            
            # Render the HTML email template and convert it to a plain text version
            email_html_message = render_to_string(email_template, email_context)
            email_plain_message = strip_tags(email_html_message)
            # Set up the email parameters
            from_email = getattr(settings, 'EMAIL_HOST_USER', 'default_from_email')
            to_email = email

            # Create the EmailMessage object
            email_message = EmailMessage(
                subject=email_subject,
                body=email_plain_message,
                from_email=from_email,
                to=[to_email]
            )
            email_message.send()
            
            messages.success(request,"Successfully Added Manager")
            return HttpResponseRedirect(reverse("add_manager"))
        except:
            messages.error(request,"Failed to Add Manager")
            return HttpResponseRedirect(reverse("add_manager"))



@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def edit_hr(request,hr_id):
    manager = CustomUser.objects.filter(user_type=4)
    hr=HRs.objects.get(admin=hr_id)
    if request.user.user_type=='1':
        return render(request,"hr_management/admin/edit_hr_template.html",{"hr":hr,"id":hr_id,'manager':manager})
    else:
        return render(request,"hr_management/hr/edit_hr_template.html",{"hr":hr,"id":hr_id,'manager':manager})


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def edit_hr_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        hr_id=request.POST.get("hr_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")
        manager= request.POST.get('manager')

        try:
            user=CustomUser.objects.get(id=hr_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.manager = manager
            user.save()

            hr_model=HRs.objects.get(admin=hr_id)
            hr_model.address=address
            hr_model.save()
            messages.success(request,"Successfully Edited Staf HR")
            return redirect('manage_hr')
        except:
            messages.error(request,"Failed to Edit HR")




@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def edit_employee(request,employee_id):
    manager = CustomUser.objects.filter(user_type=4)
    employee=Employees.objects.get(admin=employee_id)
    if request.user.user_type == '2':
        return render(request,"hr_management/hr/edit_employee_template.html",{"employee":employee,"id":employee_id,'manager':manager})
    else:
        return render(request,"hr_management/admin/edit_employee_template.html",{"employee":employee,"id":employee_id,'manager':manager})


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def edit_employee_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        employee_id=request.POST.get("employee_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        manager= request.POST.get('manager')
        designation = request.POST.get("designation")
        department = request.POST.get("department")

        try:
            user=CustomUser.objects.get(id=employee_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.manager = manager
            user.save()
            employee_model=Employees.objects.get(admin=employee_id)
            employee_model.designation=designation
            employee_model.department=department
            employee_model.save()
            messages.success(request,"Successfully Edited Employee")
            return redirect('manage_employee')
        except:
            messages.error(request,"Failed to Edit Manager")


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def delete_employee(request, employee_id):
    user = CustomUser.objects.get(id=employee_id)
    context ={'user':user}
    if request.method == 'POST':
         user.delete()
         messages.success(request, "Employee Deleted Successfully")
         return HttpResponseRedirect(reverse('manage_employee'))
    if request.user.user_type == '2':
        return render(request,'hr_management/hr/delete_employee_template.html',context)
    else:
        return render(request,'hr_management/admin/delete_employee_template.html',context)




@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def delete_hr(request, hr_id):
    try:
        user = CustomUser.objects.get(id=hr_id)
        context ={'user':user}
        if request.method == 'POST':
            user.delete()
            messages.success(request, "HR Deleted Successfully")
            return HttpResponseRedirect(reverse('manage_hr'))
        if request.user.user_type == '1':
            return render(request,'hr_management/admin/delete_hr_template.html',context)
        else:
            return render(request,'hr_management/hr/delete_hr_template.html',context)
    except BaseException as a:
        print(a)


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def employee_details(request, employee_id):
    try:
        user = CustomUser.objects.get(id=employee_id)
        employee=Employees.objects.get(admin=user)
        personal_info = Employee_Onboarding.objects.filter(employee=employee)
        current_address = Address_detail.objects.filter(employee=employee)
        per_address = Permanent_Address.objects.filter(employee=employee)
        emp_family_details = FamilyDetails.objects.filter(employee=employee)
        bank_details =BankDetails.objects.filter(employee=employee)
        documents = Documents.objects.filter(employee=employee)
        
    except CustomUser.DoesNotExist:
        messages.error(request, 'Employee Not Available')
    
    context = {'user':user,'personal_info': personal_info, 'current_address': current_address, 'per_address':per_address,'emp_family_details':emp_family_details,'bank_details':bank_details,'documents': documents} 
    if request.user.user_type == '2':
        return render(request, 'hr_management/hr/employee_onboarding_details.html', context)
    else:
        return render(request, 'hr_management/admin/employee_onboarding_details.html', context)


#################################### delete onboarding details #######################

@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def employee_details_delete(request, employee_id):
    user = CustomUser.objects.get(id=employee_id)
    employee = Employees.objects.get(admin=user)
    personal_info = Employee_Onboarding.objects.get(employee=employee)
    current_address = Address_detail.objects.get(employee=employee)
    per_address = Permanent_Address.objects.get(employee=employee)
    emp_family_details = FamilyDetails.objects.get(employee=employee)
    bank_details = BankDetails.objects.get(employee=employee)
    documents = Documents.objects.get(employee=employee)

    personal_info.delete()
    current_address.delete()
    per_address.delete()
    emp_family_details.delete()
    bank_details.delete()
    documents.delete()

    context = {
        'user': user,
        
    }
    if request.user.user_type == '2':
        return render(request, 'hr_management/hr/employee_onboarding_details.html', context)
    else:
        return render(request, 'hr_management/admin/employee_onboarding_details.html', context)


@login_required(login_url='do_login')
@require_user_type(user_type=[1,4])
def employee_leave_view(request):
    # Get all leave requests
    leaves = LeaveReportEmployee.objects.all()
    
    # Approve pending leave requests that have been pending for more than 7 day
    for leave in leaves:
        if leave.leave_status == 0:
            leave_start_date = datetime.strptime(str(leave.leave_start_date), "%Y-%m-%d").date()
            time_since_request = datetime.now().date() - leave_start_date
            if time_since_request >= timedelta(days=7):
                # Approve the leave request
                leave.leave_status = 1
                leave.save()
        
    # Get all leave requests again
    leaves = LeaveReportEmployee.objects.all()
    
    # Render the template with the leave requests and current time
    if request.user.user_type == '4':
        return render(request, "hr_management/manager_template/employee_leave_view.html", {"leaves": leaves, "current_time": datetime.now()})
    else:
        return render(request, "hr_management/admin/employee_leave_view.html", {"leaves": leaves, "current_time": datetime.now()})


@login_required(login_url='do_login')
@require_user_type(1)
def manage_session(request):
    return render(request,"hr_management/admin/manage_session_template.html")

# @login_required(login_url='do_login')
# @require_user_type(1)
# def add_session_save(request):
#     if request.method!="POST":
#         return HttpResponseRedirect(reverse("manage_session"))
#     else:
#         session_start_year=request.POST.get("session_start")
#         session_end_year=request.POST.get("session_end")

#         try:
#             messages.success(request, "Successfully Added Session")
#             return HttpResponseRedirect(reverse("manage_session"))
#         except:
#             messages.error(request, "Failed to Add Session")
#             return HttpResponseRedirect(reverse("manage_session"))


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@login_required(login_url='do_login')
@require_user_type(1)
def hr_feedback_message(request):
    feedbacks=FeedBackHRs.objects.all()
    return render(request,"hr_management/admin/hr_feedback_template.html",{"feedbacks":feedbacks})


@login_required(login_url='do_login')
@require_user_type(1)
def employee_feedback_message(request):
    feedbacks=FeedBackEmployee.objects.all()
    return render(request,"hr_management/admin/employee_feedback_template.html",{"feedbacks":feedbacks})

@login_required(login_url='do_login')
@require_user_type(1)
@csrf_exempt
def employee_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackEmployee.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@login_required(login_url='do_login')
@require_user_type(1)
@csrf_exempt
def hr_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackHRs.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def hr_leave_view(request):
    leaves=LeaveReportHR.objects.all()
    if request.user.user_type == '2':
        return render(request,"hr_management/hr/hr_leave_view.html",{"leaves":leaves})
    else:
        return render(request,"hr_management/admin/hr_leave_view.html",{"leaves":leaves})


@login_required(login_url='do_login')
@require_user_type(user_type=[1,4])
def employee_approve_leave(request, leave_id):
    
    leave = LeaveReportEmployee.objects.filter(id=leave_id).first()
    emp_id = leave.employee_id
    leave.leave_status = 1
    leave.save()  
    first_name = emp_id.admin.first_name
    last_name = emp_id.admin.last_name
    employee_leave = EmployeeLeave.objects.filter(employee_id=emp_id).first()

    leave_start_date_str = leave.leave_start_date.strftime('%Y-%m-%d')
    leave_end_date_str = leave.leave_end_date.strftime('%Y-%m-%d')

    leave_start_date = datetime.strptime(leave_start_date_str, '%Y-%m-%d').date()
    leave_end_date = datetime.strptime(leave_end_date_str, '%Y-%m-%d').date()

    # Calculate the number of days between leave_start_date and leave_end_date
    num_days = (leave_end_date - leave_start_date).days + 1
    excluded_days = 0
    for i in range(num_days):
        date = leave_start_date + timedelta(days=i)
        if date.weekday() >= 5:  
            excluded_days += 1

    num_days -= excluded_days

    if leave.leave_type == 'Earned':
        employee_leave.EarnLeave_used += num_days
        
        if employee_leave.current_EL < num_days:
            abc = num_days - employee_leave.current_EL
            employee_leave.current_EL = 0
            employee_leave.Prev_CFEL = employee_leave.Prev_CFEL - abc 
        else:
            employee_leave.current_EL = employee_leave.current_EL - num_days 

        
        employee_leave.EarnLeave = employee_leave.Prev_CFEL + employee_leave.current_EL
        employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave

    elif leave.leave_type == 'casual':
        total_Used_casual_leaves = employee_leave.CasualLeave_used + num_days
        employee_leave.CasualLeave_used = total_Used_casual_leaves
        employee_leave.CasualLeave = employee_leave.CasualLeave - total_Used_casual_leaves
        employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave

    employee_leave.save()
    email_subject = 'Leave Request Approved'
    email_template = 'hr_management/admin/leave_request_approved.html'  # Path to your email template
    email_context = {'employee': employee_leave,'first_name':first_name,'last_name':last_name,'leave_start_date':leave_start_date,'leave_end_date':leave_end_date}  # Context data for the template

    # Render the HTML email template and convert it to a plain text version
    email_html_message = render_to_string(email_template, email_context)
    email_plain_message = strip_tags(email_html_message)

    # Set up the email parameters
    from_email = getattr(settings, 'EMAIL_HOST_USER', 'default_from_email')
    to_email = emp_id.admin.email

    # Create the EmailMessage object
    email_message = EmailMessage(
        subject=email_subject,
        body=email_plain_message,
        from_email=from_email,
        to=[to_email]
    )
    email_message.send()
    return HttpResponseRedirect(reverse("employee_leave_view"))



@login_required(login_url='do_login')
@require_user_type(1)
def employee_disapprove_leave(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
        

    # Get the associated CustomUser instance
    employee = leave.employee_id
    first_name = employee.admin.first_name
    last_name = employee.admin.last_name
    

    # Send email notification
    email_subject = 'Leave Request Disapproved'
    email_template = 'hr_management/admin/leave_request_disapproved.html'  # Path to your email template
    email_context = {'employee': employee, 'first_name': first_name, 'last_name': last_name}  # Context data for the template

    # Render the HTML email template and convert it to a plain text version
    email_html_message = render_to_string(email_template, email_context)
    email_plain_message = strip_tags(email_html_message)

    # Set up the email parameters
    from_email = getattr(settings, 'EMAIL_HOST_USER', 'default_from_email')
    to_email = employee.admin.email

    # Create the EmailMessage object
    email_message = EmailMessage(
        subject=email_subject,
        body=email_plain_message,
        from_email=from_email,
        to=[to_email]
    )

    # Attach the HTML content

    # Send the email
    email_message.send()

    return HttpResponseRedirect(reverse("employee_leave_view"))


@login_required(login_url='do_login')
@require_user_type(1)
def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hr_management/admin/admin_profile.html",{"user":user})


@login_required(login_url='do_login')
@require_user_type(1)
def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))



@login_required(login_url='do_login')
@require_user_type(1)
@csrf_exempt
def admin_send_notification_employee(request):
    employees=Employees.objects.all()
    return render(request,"hr_management/admin/employee_notification.html",{"employees":employees})



@login_required(login_url='do_login')
@require_user_type(1)
def admin_send_notification_hr(request):
    hrs=HRs.objects.all()
    return render(request,"hr_management/admin/hr_notification.html",{"hrs":hrs})



@login_required(login_url='do_login')
@require_user_type(1)
@csrf_exempt
def send_employee_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    employee=Employees.objects.get(admin=id)
    token=employee.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"HR Management System",
            "body":message,
            "click_action": "https://hrmanagementsystem22.herokuapp.com/employee_all_notification",
            "icon": "http://hrmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationEmployee(employee_id=employee,message=message)
    notification.save()
    return HttpResponse("True")



@login_required(login_url='do_login')
@require_user_type(1)
@csrf_exempt
def send_hr_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    hr=HRs.objects.get(admin=id)
    token=hr.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"HR Management System",
            "body":message,
            "click_action":"https://hrmanagementsystem22.herokuapp.com/hr_all_notification",
            "icon":"http://hrmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationHRs(hr_id=hr,message=message)
    notification.save()
    return HttpResponse("True")

###################################### TO GENERATE PDF ###################################
import weasyprint
@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def generate_offer_letter(request):
    try:
        if request.method == 'POST':
            offer_letter_sended = OfferLetter_Sended()
            offer_letter_sended.ctc = float(request.POST.get('ctc'))
            offer_letter_sended.name = request.POST.get('name')
            offer_letter_sended.email = request.POST.get('email')
            offer_letter_sended.offer_release_date = request.POST.get('offer_release_date')
            offer_letter_sended.joining_date = request.POST.get('joining_date')
            offer_letter_sended.reporting = request.POST.get('reporting')
            offer_letter_sended.address = request.POST.get('address')
            offer_letter_sended.designation = request.POST.get('designation')
            offer_letter_sended.job_grade = request.POST.get('job_grade')
            offer_letter_sended.hr_name = request.POST.get('hr_name')
            offer_letter_sended.offer_accept_date = request.POST.get('offer_accept_date')
            offer_letter_sended.mobile_no = request.POST.get('mobile_no')

            formatted_date = datetime.strptime(offer_letter_sended.offer_release_date, '%Y-%m-%d').strftime('%d%m%Y')

            name = request.POST.get('name') 
            offer_release_date = request.POST.get('offer_release_date')
            amount = offer_letter_sended.ctc
            amount_words = num2words(amount)
            joining_date = request.POST.get('joining_date')
            time = request.POST.get('time')
            address = request.POST.get('address')
            designation = request.POST.get('designation')
            job_grade = request.POST.get('job_grade')
            reporting = request.POST.get('reporting')
            hr_name = request.POST.get('hr_name')
            offer_accept_date = request.POST.get('offer_accept_date')
            ctc = offer_letter_sended.ctc


            insurance_premiums = float(11000)
            total_variable_pay = ctc * 0.10
            total_fixed_pay = ctc - total_variable_pay - insurance_premiums
            basic_pay = total_fixed_pay * 0.40
            employer_pf_contribution = 0.13 * basic_pay
            hra = 0.50 * basic_pay
            flexible_components_tfp = total_fixed_pay - basic_pay - hra - employer_pf_contribution
            total_cost_to_company = total_fixed_pay + total_variable_pay + insurance_premiums


    #         # Calculate ESIC and insurance_premiums values
            if ctc <=  252000:
                esic = 0.0325 * ctc
                insurance_premiums = 0
            else:
                esic = 0
                insurance_premiums = 11000.0
            
            offer_letter = OfferLetter(
                basic_pay=basic_pay,
                hra=hra,
                total_fixed_pay=total_fixed_pay,
                total_variable_pay=total_variable_pay,
                insurance_premiums=insurance_premiums,
                total_cost_to_company=total_cost_to_company,
                employer_pf_contribution=employer_pf_contribution,
                flexible_components_tfp=flexible_components_tfp,
                esic = esic
            )

            offer_letter.save()
            offer_letter_sended.offerletter_id = offer_letter.id
            offer_letter_id = offer_letter_sended.offerletter_id
            offer_letter_sended.save()

            if request.user.user_type == '1':
            # Render offer letter HTML template
                offer_letter_html = render_to_string('hr_management/admin/offer_letter.html', {'offer_letter': offer_letter, \
                                                    'name': name, 'amount_words': amount_words,'joining_date':joining_date,\
                                                    'reporting':reporting, 'time':time,'address':address,'offer_release_date':offer_release_date,\
                                                    'designation':designation,'job_grade':job_grade,'offer_letter_id':offer_letter_id,'hr_name':hr_name,\
                                                    'offer_accept_date':offer_accept_date, 'formatted_date':formatted_date, 'esic':esic}, request=request)

                # Create a PDF file from HTML template
                pdf_file = BytesIO()
                weasyprint.HTML(string=offer_letter_html, base_url=request.build_absolute_uri()).write_pdf(pdf_file)

                # Create and return the PDF response
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="offer_letter.pdf"'
                response.write(pdf_file.getvalue())
                return response
            else:
                offer_letter_html = render_to_string('hr_management/hr/offer_letter.html', {'offer_letter': offer_letter, \
                                                    'name': name, 'amount_words': amount_words,'joining_date':joining_date,\
                                                    'reporting':reporting, 'time':time,'address':address,'offer_release_date':offer_release_date,\
                                                    'designation':designation,'job_grade':job_grade,'offer_letter_id':offer_letter_id,'hr_name':hr_name,\
                                                    'offer_accept_date':offer_accept_date, 'formatted_date':formatted_date, 'esic':esic}, request=request)

                # Create a PDF file from HTML template
                pdf_file = BytesIO()
                weasyprint.HTML(string=offer_letter_html, base_url=request.build_absolute_uri()).write_pdf(pdf_file)

                # Create and return the PDF response
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="offer_letter.pdf"'
                response.write(pdf_file.getvalue())
                return response
        if request.user.user_type == '1':
            return render(request, 'hr_management/admin/generate_offer_letter.html')
        else:
            return render(request, 'hr_management/hr/generate_offer_letter.html')
    except:
        messages.error(request,"Please put requited details")
        return HttpResponseRedirect(reverse("generate_offer_letter"))



###############################################All Offer Letter Sended Record #######################################
from django.core.paginator import Paginator
@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def offer_letter_sended_history(request):
    offer_letters_sended = OfferLetter_Sended.objects.all()
    paginator = Paginator(offer_letters_sended, 10)  # 10 items per page
    page = request.GET.get('page')
    offer_letters_sended = paginator.get_page(page)
    if request.user.user_type == '1':
        return render(request, 'hr_management/admin/offer_letter_sended_history.html', {'offer_letters_sended': offer_letters_sended})
    else:
        return render(request, 'hr_management/hr/offer_letter_sended_history.html', {'offer_letters_sended': offer_letters_sended})

###########################################Payroll###################################################
@login_required(login_url='do_login')
@require_user_type(1)
def payroll(request):
    template_name = 'hr_management/admin/payroll.html'
    context = {}
    return render(request,template_name, context)

###########################################Generate wage register ###################################################


@login_required(login_url='do_login')
@require_user_type(1)
def employee_wage_register_details(request):
    employees = Employee_Onboarding.objects.all()
    wage_registers = []
    
    for employee in employees:
        last_wage_register = WageRegister.objects.filter(employee_id=employee.id).order_by('-id').first()
        wage_registers.append(last_wage_register)
    
    return render(request, 'hr_management/admin/wage_register.html', {'employees': employees, 'wage_registers': wage_registers})


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def wage_register(request):
    try:
        employees = Employee_Onboarding.objects.all()
        wage_registers = []
        today = date.today()
        salary_drop = SalarySlip.objects.all()   

        available_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            
        current_year = datetime.now().year
        start_year = 2021

        available_years = [str(year) for year in range(start_year, current_year + 2)]

        remaining_years = {}

        for year in available_years:
            remaining_months = []
            for month in available_months:
                if not any(w.year == year and w.month == month for w in salary_drop):
                    remaining_months.append(month)
            if remaining_months:
                remaining_years[year] = remaining_months          
        
        if request.method == "POST":
            month = request.POST.get('month_name')
            year = request.POST.get('year')
            days_payable = int(request.POST.get('days'))
            days_paid = int(request.POST.get('paid'))      

            month_to_number = {
                'january': 1,
                'february': 2,
                'march': 3,
                'april': 4,
                'may': 5,
                'june': 6,
                'july': 7,
                'august': 8,
                'september': 9,
                'october': 10,
                'november': 11,
                'december': 12
            }

            month_number = month_to_number.get(month.lower())
            existing_data = WageRegister.objects.filter(month=month, year=year)
            existing_data.delete()


            for employee in employees:
                employee_id = employee.id
                onboarding_data = Employee_Onboarding.objects.get(id=employee_id)
                c = onboarding_data.contact_no

                offer = OfferLetter_Sended.objects.get(mobile_no=c)
                ctc = offer.ctc
                address = offer.address

                age = today.year - employee.dob.year

                # Check if the birth month and day have already passed in the current year
                if today.month < employee.dob.month or (today.month == employee.dob.month and today.day < employee.dob.day):
                    age -= 1
                age = age

                if employee_id:
                    onboarding_data = get_object_or_404(Employee_Onboarding, id=employee_id)
                    employee = onboarding_data.employee

                    if ctc <= 252000:
                        insurance_premiums = 0
                    else:
                        insurance_premiums = 11000.0

                    variable_component = (ctc * 0.10)
                    total_variable_pay = ctc * 0.10
                    total_fixed_pay = ctc - total_variable_pay - insurance_premiums
                    basic_pay = total_fixed_pay * 0.40
                    employer_pf_contribution = 0.13 * basic_pay
                    hra = 0.50 * basic_pay
                    total_flexible_component = total_fixed_pay - basic_pay - hra - employer_pf_contribution
                    conveyance_allowance = 1600 / int(days_payable) * int(days_paid)
                    professional_tax = 200
                    income_tax = 0

                    total_variable_pay = ctc * 0.10
                    total_fixed_pay = ((ctc) - (insurance_premiums + variable_component)) / 12 * int(days_paid) / int(days_payable)
                    basic_salary = (total_fixed_pay * 0.40)
                    variable_component = (ctc * 0.10) / 12 * int(days_paid) / int(days_payable)
                    hra = 0.50 * basic_salary
                    provident_fund = 0.12 * basic_salary
                    flexible_component = (total_flexible_component / 12) * days_paid / days_payable - conveyance_allowance
                    gross_salary = (hra + basic_salary + conveyance_allowance + flexible_component + variable_component)
                    flexible_component = gross_salary - basic_salary - hra - conveyance_allowance - variable_component
                    other_deductions = 0
                    if ctc <= 252000:
                        esic = (0.0075 * float(gross_salary))
                    else:
                        esic = 0
                    total_deductions = provident_fund + professional_tax + income_tax + other_deductions +esic
                    net_salary = Decimal(gross_salary) - Decimal(total_deductions)

                    ytd_net_salary = net_salary
                    ytd_basic_salary = basic_salary
                    ytd_hra = hra
                    ytd_conveyance_allowance = conveyance_allowance
                    ytd_flexible_component = flexible_component
                    ytd_variable_component = variable_component
                    ytd_provident_fund = provident_fund
                    ytd_esic = esic
                    ytd_professional_tax = professional_tax
                    ytd_income_tax = income_tax
                    ytd_other_deductions = other_deductions
                    ytd_total_deductions = total_deductions
                    ytd_gross_salary = gross_salary

                    prev_wage_register = WageRegister.objects.filter(employee_id=employee).order_by('-id')[0:1]

                    if prev_wage_register:
                        first_salary_slip = prev_wage_register[0]
                        net_salary = first_salary_slip.net_salary
                        ytd_net_salary = first_salary_slip.ytd_net_salary
                        basic_salary = first_salary_slip.basic_salary
                        ytd_basic_salary = first_salary_slip.ytd_basic_salary
                        hra = first_salary_slip.hra
                        ytd_hra = first_salary_slip.ytd_hra
                        conveyance_allowance = first_salary_slip.conveyance_allowance
                        ytd_conveyance_allowance = first_salary_slip.ytd_conveyance_allowance
                        flexible_component = first_salary_slip.flexible_component
                        ytd_flexible_component = first_salary_slip.ytd_flexible_component
                        variable_component = first_salary_slip.variable_component
                        ytd_variable_component = first_salary_slip.variable_component
                        provident_fund = first_salary_slip.provident_fund
                        ytd_provident_fund = first_salary_slip.ytd_provident_fund
                        esic = first_salary_slip.esic
                        ytd_esic = first_salary_slip.ytd_esic
                        professional_tax = first_salary_slip.professional_tax
                        ytd_professional_tax = first_salary_slip.ytd_professional_tax
                        income_tax = first_salary_slip.income_tax
                        ytd_income_tax = first_salary_slip.ytd_income_tax
                        other_deductions = first_salary_slip.other_deductions
                        ytd_other_deductions = first_salary_slip.ytd_other_deductions
                        total_deductions = first_salary_slip.total_deductions
                        ytd_total_deductions = first_salary_slip.ytd_total_deductions
                        gross_salary = first_salary_slip.gross_salary
                        ytd_gross_salary = first_salary_slip.ytd_gross_salary

                        if month_number == 4:  # Check if the month is April or later
                            ytd_net_salary = net_salary
                            ytd_basic_salary = basic_salary
                            ytd_hra = hra
                            ytd_conveyance_allowance = conveyance_allowance
                            ytd_flexible_component = flexible_component
                            ytd_variable_component = variable_component
                            ytd_provident_fund = provident_fund
                            ytd_esic = esic
                            ytd_professional_tax = professional_tax
                            ytd_income_tax = income_tax
                            ytd_other_deductions = other_deductions
                            ytd_total_deductions = total_deductions
                            ytd_gross_salary = gross_salary
                        else:
                            ytd_net_salary += net_salary
                            ytd_basic_salary += basic_salary
                            ytd_hra += hra
                            ytd_conveyance_allowance += conveyance_allowance
                            ytd_flexible_component += flexible_component
                            ytd_variable_component += variable_component
                            ytd_provident_fund += provident_fund
                            ytd_esic += esic
                            ytd_professional_tax += professional_tax
                            ytd_income_tax += income_tax
                            ytd_other_deductions += other_deductions
                            ytd_total_deductions += total_deductions
                            ytd_gross_salary += gross_salary

                    wage_register = WageRegister(
                        employee_id=employee,
                        month=month,
                        year=year,
                        age = age,
                        days_payable=days_payable,
                        days_paid=days_paid,
                        ctc=round(ctc),
                        esic=round(esic),
                        basic_salary=round(basic_salary),
                        hra=round(hra),
                        conveyance_allowance=round(conveyance_allowance),
                        flexible_component=round(flexible_component),
                        variable_component=round(variable_component),
                        provident_fund=round(provident_fund),
                        professional_tax=round(professional_tax),
                        income_tax=round(income_tax),
                        other_deductions=round(other_deductions),
                        gross_salary=round(gross_salary),
                        total_deductions=round(total_deductions),
                        net_salary=round(net_salary),
                        address=address,
                        ytd_net_salary=round(ytd_net_salary),
                        ytd_basic_salary=round(ytd_basic_salary),
                        ytd_hra=round(ytd_hra),
                        ytd_conveyance_allowance=round(ytd_conveyance_allowance),
                        ytd_flexible_component=round(ytd_flexible_component),
                        ytd_variable_component=round(ytd_variable_component),
                        ytd_provident_fund=round(ytd_provident_fund),
                        ytd_esic=round(ytd_esic),
                        ytd_professional_tax=round(ytd_professional_tax),
                        ytd_income_tax=round(ytd_income_tax),
                        ytd_other_deductions=round(ytd_other_deductions),
                        ytd_total_deductions=round(ytd_total_deductions),
                        ytd_gross_salary=round(ytd_gross_salary)
                    )
                    
                    wage_register.save()
                    wage_registers.append(wage_register)
                        
            if request.user.user_type == '1':
                return render(request, 'hr_management/admin/wage_register.html', {'employees': employees, 'wage_registers': wage_registers,'age':age,'month':month,'year':year})
            else:
                return render(request, 'hr_management/hr/wage_register.html', {'employees': employees, 'wage_registers': wage_registers,'age':age,'month':month,'year':year})
        if request.user.user_type == '1':
            return render(request, 'hr_management/admin/employee_salary_all.html', {'employees': employees,'remaining_years':remaining_years})
        else:
            return render(request, 'hr_management/hr/employee_salary_all.html', {'employees': employees,'remaining_years':remaining_years})

    except:
        messages.error(request,"Please fill required details")
        return HttpResponseRedirect(reverse("wage_register"))



@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def old_wage_register(request):
    salary_slips = WageRegister.objects.all()
    unique_months = set()
    unique_years = set()
    for slip in salary_slips:
            unique_months.add(slip.month)
            unique_years.add(slip.year)

    if request.method == 'POST':    
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        if selected_month:
            salary_slips = salary_slips.filter(month=selected_month)

        if selected_year:
            salary_slips = salary_slips.filter(year=selected_year)

        old_wage_registers = salary_slips
        selected_salary_slip = old_wage_registers.first()
        if not selected_salary_slip:
            if request.user.user_type == '2':
                return render(request, 'hr_management/hr/wage_register_not_generated.html')
            else:
                return render(request, 'hr_management/admin/wage_register_not_generated.html')
            
        if request.user.user_type == '1':
            return render(request, 'hr_management/admin/old_wage_register.html', {
                "salary_slips": salary_slips,
                "old_wage_registers": old_wage_registers,
                "selected_salary_slip": selected_salary_slip,
                "unique_months": unique_months,  # Pass unique_months to the template
                "unique_years": unique_years,  # Pass unique_years to the template
            })
        else:
            return render(request, 'hr_management/hr/old_wage_register.html', {
                "salary_slips": salary_slips,
                "old_wage_registers": old_wage_registers,
                "selected_salary_slip": selected_salary_slip,
                "unique_months": unique_months,  # Pass unique_months to the template
                "unique_years": unique_years,  # Pass unique_years to the template
            })
    if request.user.user_type == '1':
        return render(request, 'hr_management/admin/old_wage_register.html',{'unique_months':unique_months,"unique_years": unique_years})
    else:
        return render(request, 'hr_management/hr/old_wage_register.html',{'unique_months':unique_months,"unique_years": unique_years})

#########################################################################################################################
@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def generate_salary_slips(request):
    emp = Employees.objects.all()
    salary_slips = []

    # Get the last wage register for each employee
    for employee in emp:
        wage_register = WageRegister.objects.filter(employee_id=employee).last()

        if wage_register is not None:
            employee_id = wage_register.employee_id.id
            onboarding_data = Employee_Onboarding.objects.get(employee_id=employee_id)
            c = onboarding_data.contact_no

            offer = OfferLetter_Sended.objects.get(mobile_no=c)
            # ctc = offer.ctc
            address = offer.address

            salary_slip = SalarySlip(
                employee_id=employee,
                basic_salary=wage_register.basic_salary,
                conveyance_allowance=wage_register.conveyance_allowance,
                total_deductions=wage_register.total_deductions,
                gross_salary=wage_register.gross_salary,
                net_salary=wage_register.net_salary,
                ctc=wage_register.ctc,
                hra=wage_register.hra,
                esic=wage_register.esic,
                flexible_component=wage_register.flexible_component,
                variable_component=wage_register.variable_component,
                provident_fund=wage_register.provident_fund,
                professional_tax=wage_register.professional_tax,
                income_tax=wage_register.income_tax,
                other_deductions=wage_register.other_deductions,
                other_allowns=wage_register.other_allowns,
                lwf=wage_register.lwf,
                ytd_ctc=wage_register.ytd_ctc,
                ytd_hra=wage_register.ytd_hra,
                ytd_esic=wage_register.ytd_esic,
                ytd_basic_salary=wage_register.ytd_basic_salary,
                ytd_conveyance_allowance=wage_register.ytd_conveyance_allowance,
                ytd_flexible_component=wage_register.ytd_flexible_component,
                ytd_variable_component=wage_register.ytd_variable_component,
                ytd_provident_fund=wage_register.ytd_provident_fund,
                ytd_professional_tax=wage_register.ytd_professional_tax,
                ytd_income_tax=wage_register.ytd_income_tax,
                ytd_other_deductions=wage_register.ytd_other_deductions,
                ytd_gross_salary=wage_register.ytd_gross_salary,
                ytd_total_deductions=wage_register.ytd_total_deductions,
                ytd_net_salary=wage_register.ytd_net_salary,
                days_payable=wage_register.days_payable,
                days_paid=wage_register.days_paid,
                address=address,
                month=wage_register.month,
                year=wage_register.year,
            )
            salary_slip.save()
            salary_slips.append(salary_slip)
    if request.user.user_type == '2':
        return render(request, 'hr_management/hr/salary_slip_generate_successfully.html')
    else:
        return render(request, 'hr_management/admin/salary_slip_generate_successfully.html')



# ################################Update wage register ##############################################

@login_required(login_url='do_login')
@require_user_type(1)               
def edit_wage_register(request, pk):
    wage_register = get_object_or_404(WageRegister, id=pk)
    employees = Employee_Onboarding.objects.all()

    if request.method == "POST":
        ctc = float(request.POST.get('ctc'))
        wage_register.month = request.POST.get('month')
        wage_register.year = request.POST.get('year')
        days_payable = Decimal(request.POST.get('days_payable'))
        days_paid = Decimal(request.POST.get('days_paid'))
        wage_register.days_payable = days_payable
        wage_register.days_paid = days_paid
        wage_register.basic_salary = Decimal(request.POST.get('basic_salary'))
        wage_register.hra = Decimal(request.POST.get('hra'))
        wage_register.conveyance_allowance = Decimal(request.POST.get('conveyance_allowance'))
        wage_register.variable_component = Decimal(request.POST.get('variable_component'))
        wage_register.other_allowns = Decimal(request.POST.get('other_allowns'))
        wage_register.gross_salary = Decimal(request.POST.get('gross_salary'))
        wage_register.provident_fund = Decimal(request.POST.get('provident_fund'))
        wage_register.professional_tax = Decimal(request.POST.get('professional_tax'))
        wage_register.income_tax = Decimal(request.POST.get('income_tax'))
        wage_register.lwf = Decimal(request.POST.get('lwf'))
        wage_register.gross_salary = Decimal(request.POST.get('gross_salary'))
        wage_register.other_deductions = Decimal(request.POST.get('other_deductions'))
        wage_register.net_salary = Decimal(request.POST.get('net_salary'))
        wage_register.esic = Decimal(request.POST.get('esic'))
    

        hra = 0
        esic = 0
        basic_salary = 0
        conveyance_allowance = 0
        flexible_component = 0
        variable_component = 0
        provident_fund = 0
        professional_tax = 0
        income_tax = 0
        other_deductions = 0
        gross_salary = 0
        total_deductions = 0
        net_salary = 0


        ytd_hra = hra
        ytd_ctc = ctc
        ytd_esic = esic
        ytd_basic_salary = basic_salary
        ytd_conveyance_allowance = conveyance_allowance
        ytd_flexible_component = flexible_component
        ytd_variable_component = variable_component
        ytd_provident_fund = provident_fund
        ytd_professional_tax = professional_tax
        ytd_income_tax = income_tax
        ytd_other_deductions = other_deductions
        ytd_gross_salary = gross_salary
        ytd_total_deductions = total_deductions
        ytd_net_salary = net_salary
   
        
        for employee in employees:
            employee_id = employee.id

            if employee_id:
                    if ctc <= 252000:
                        insurance_premiums = 0
                    else:
                        insurance_premiums = 11000.0
                    variable_component = (ctc * 0.10)
                    # Calculate salary components
                    total_variable_pay = ctc * 0.10
                    total_fixed_pay = ctc - total_variable_pay - insurance_premiums
                    basic_pay = total_fixed_pay * 0.40
                    employer_pf_contribution = 0.13 * basic_pay
                    hra = 0.50 * basic_pay
                    total_flexible_component = total_fixed_pay - basic_pay - hra - employer_pf_contribution
                    conveyance_allowance = 1600/ int(days_payable) * int(days_paid)
                    professional_tax = 200
                    income_tax = float(wage_register.income_tax)

                    # Calculate salary components for 5 working days
                    total_variable_pay = ctc * 0.10
                    total_fixed_pay = ((ctc) - (insurance_premiums + variable_component)) / 12 * int(days_paid)/int(days_payable)
                    basic_salary = (total_fixed_pay * 0.40)
                    variable_component = (ctc * 0.10) / 12 * int(days_paid)/int(days_payable)
                    hra = 0.50 * basic_salary

                    wage_register.ytd_hra = hra + float(wage_register.ytd_hra)
                    wage_register.ytd_ctc = ctc + float(wage_register.ytd_ctc)
                    wage_register.ytd_esic = esic + float(wage_register.ytd_esic)
                    wage_register.ytd_basic_salary = basic_salary+ float(wage_register.ytd_basic_salary)
                    wage_register.ytd_conveyance_allowance = conveyance_allowance
                    wage_register.ytd_flexible_component = flexible_component
                    wage_register.ytd_variable_component = variable_component
                    wage_register.ytd_provident_fund = provident_fund
                    wage_register.ytd_professional_tax = professional_tax
                    wage_register.ytd_income_tax = income_tax
                    wage_register.ytd_other_deductions = float(other_deductions)
                    wage_register.ytd_gross_salary = gross_salary
                    wage_register.ytd_total_deductions = total_deductions
                    wage_register.ytd_net_salary = net_salary
                   

                    provident_fund = 0.12 * basic_salary
                    flexible_component = (total_flexible_component / 12) * int(days_paid)/int(days_payable) - conveyance_allowance
                    gross_salary = hra + basic_salary + conveyance_allowance + flexible_component + variable_component + float(wage_register.other_allowns)
                    
                    if ctc <= 252000:
                        esic = 0.0075 * float(gross_salary)

                    else:
                        esic = 0
                    flexible_component = gross_salary - basic_salary - hra - conveyance_allowance - variable_component
                    other_deductions = wage_register.other_deductions
                    total_deductions = provident_fund + professional_tax + income_tax + float(other_deductions)
                
                    wage_register.basic_salary=round(basic_salary)
                    wage_register.hra= round(hra)
                    wage_register.conveyance_allowance= round(conveyance_allowance)
                    wage_register.variable_component= round(variable_component)
                    wage_register.gross_salary= round(gross_salary)
                    wage_register.flexible_component= round(flexible_component) 
                    wage_register.professional_tax = round( professional_tax)
                    wage_register.provident_fund = round( provident_fund)
                    total_deductions = round( (
                        float(wage_register.provident_fund) +
                        float(wage_register.professional_tax) +
                        float(wage_register.income_tax) +
                        float(wage_register.other_deductions)+
                        float(wage_register.esic)
                    ))
                    wage_register.total_deductions = round(total_deductions)
                    wage_register.esic = round(esic)
                    net_salary = round(float(wage_register.gross_salary) -float(wage_register.total_deductions))
                    wage_register.net_salary = round(net_salary)
                                            

                    wage_register.ytd_hra = round(ytd_hra)
                    wage_register.ytd_ctc = round(ytd_ctc) 
                    wage_register.ytd_esic = round(ytd_esic)
                    wage_register.ytd_basic_salary= round(ytd_basic_salary)
                    wage_register.ytd_conveyance_allowance = round(ytd_conveyance_allowance)
                    wage_register.ytd_variable_component = round(ytd_variable_component)
                    wage_register.ytd_provident_fund = round(ytd_provident_fund)
                    wage_register.ytd_professional_tax = round(ytd_professional_tax)
                    wage_register.ytd_income_tax = round(ytd_income_tax)
                    wage_register.ytd_other_deductions = round(ytd_other_deductions)
                    wage_register.ytd_total_deductions = round(ytd_total_deductions)
                    wage_register.ytd_gross_salary = round(ytd_gross_salary)
                    wage_register.ytd_net_salary = round(ytd_net_salary)
                    wage_register.ytd_flexible_component = round(ytd_flexible_component)

                    if wage_register.month == 'April':  # Check if the month is April or later
                        wage_register.ytd_basic_salary = round(basic_salary)
                        wage_register.ytd_hra = round(hra)
                        wage_register.ytd_ctc = round(ctc)
                        wage_register.ytd_net_salary = round(net_salary)
                        wage_register.ytd_conveyance_allowance = round(conveyance_allowance)
                        wage_register.ytd_flexible_component = round(flexible_component)
                        wage_register.ytd_variable_component = round(variable_component)
                        wage_register.ytd_provident_fund = round(provident_fund)
                        wage_register.ytd_esic = round(esic)
                        wage_register.ytd_professional_tax = round(professional_tax)
                        wage_register.ytd_income_tax = round(income_tax)
                        wage_register.ytd_other_deductions = round(other_deductions)
                        wage_register.ytd_total_deductions = round(total_deductions)
                        wage_register.ytd_gross_salary = round(gross_salary)
                        wage_register.ytd_net_salary = round(net_salary)

                        
                    else:
                        wage_register.ytd_net_salary += round(int(net_salary))
                        wage_register.ytd_basic_salary += round(int(basic_salary))
                        wage_register.ytd_hra += round(Decimal(hra))
                        wage_register.ytd_ctc += round(Decimal(ctc))
                        wage_register.ytd_conveyance_allowance += round(Decimal(conveyance_allowance))
                        wage_register.ytd_flexible_component += round(Decimal(flexible_component))
                        wage_register.ytd_variable_component += round(Decimal(variable_component))
                        wage_register.ytd_provident_fund += round(Decimal(provident_fund))
                        wage_register.ytd_esic += round(float(esic))
                        wage_register.ytd_professional_tax += round(Decimal(professional_tax))
                        wage_register.ytd_income_tax += round(Decimal(income_tax))
                        wage_register.ytd_other_deductions += round(Decimal(other_deductions))
                        wage_register.ytd_total_deductions += round(Decimal(total_deductions))
                        wage_register.ytd_gross_salary += round(Decimal(gross_salary))
             
                    wage_register.save() 
                    previous_wage_registers = {}
                    wage_registers = WageRegister.objects.filter(employee_id=wage_register.employee_id).order_by('-id')

                    for idx, wage_register in enumerate(wage_registers):
                        if idx != 0:
                            previous_wage_registers[int(wage_register.id)] = int(wage_registers[idx - 1].id)
                    pre_salary = list(previous_wage_registers.keys())

                    wage_register1 = WageRegister.objects.get(id=pk)
                    wage_register2 = None  # Initialize wage_register2 with a default value

                    try:
                        wage_register2 = WageRegister.objects.get(id=pre_salary[0])
                    except:
                        pass


                    if wage_register2:
                        wage_register1.ytd_hra += round(wage_register2.ytd_hra)
                        wage_register1.ytd_esic += round(wage_register2.ytd_esic)
                        wage_register1.ytd_ctc += round(wage_register2.ytd_ctc)
                        wage_register1.ytd_basic_salary += round(wage_register2.ytd_basic_salary)
                        wage_register1.ytd_conveyance_allowance += round(wage_register2.ytd_conveyance_allowance)
                        wage_register1.ytd_variable_component += round(wage_register2.ytd_variable_component)
                        wage_register1.ytd_provident_fund += round(wage_register2.ytd_provident_fund)
                        wage_register1.ytd_professional_tax += round(wage_register2.ytd_professional_tax)
                        wage_register1.ytd_income_tax += round(wage_register2.ytd_income_tax)
                        wage_register1.ytd_other_deductions += round(wage_register2.ytd_other_deductions)
                        wage_register1.ytd_total_deductions += round(wage_register2.ytd_total_deductions)
                        wage_register1.ytd_gross_salary += round(wage_register2.ytd_gross_salary)
                        wage_register1.ytd_net_salary += round(wage_register2.ytd_net_salary)
                        wage_register1.ytd_flexible_component += round(wage_register2.ytd_flexible_component)


                    wage_register1.save()
                    return redirect('employee_wage_register_details')

    return render(request, 'hr_management/admin/edit_wage_register.html', {'wage_register': wage_register})

