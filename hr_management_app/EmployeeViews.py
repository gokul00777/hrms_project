import datetime
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from datetime import date
from .decorators import require_user_type
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from num2words import num2words
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError



@require_user_type(user_type=3)
@login_required(login_url='do_login')
def employee_home(request):
    try:
        employee_obj = Employees.objects.get(admin=request.user.id)
    except Employees.DoesNotExist:
        return redirect('do_login')
    
    employee_count = Employees.objects.filter(admin=request.user.id).count()
    leave_count = LeaveReportEmployee.objects.filter(employee_id=employee_obj, leave_status=1).count()
    data_present = []
    data_absent = []

    return render(request,"hr_management/employee_template/employee_home_template.html",{"employee_count": employee_count, "data1":data_present,"data2":data_absent,'leave_count':leave_count})

import datetime
@login_required(login_url='do_login')
@require_user_type(user_type=[3,4])
def employee_apply_leave(request):
    try:
        employee = Employees.objects.filter(admin=request.user.id).first()
        emp_leaves = EmployeeLeave.objects.filter(employee_id = employee).first()
        leave_data = LeaveReportEmployee.objects.filter(employee_id = employee)    
        current_date = datetime.datetime.now().date()
        if emp_leaves.year_updated != current_date.year:
            if emp_leaves.current_EL > 9 :
                emp_leaves.current_EL = 9
            else :
                emp_leaves.current_EL = emp_leaves.current_EL
            
            emp_leaves.Prev_CFEL = min(emp_leaves.Prev_CFEL + emp_leaves.current_EL , 45)
            emp_leaves.year_updated = current_date.year
            emp_leaves.current_EL = 1.5
            emp_leaves.CasualLeave = 0.67
                
        elif emp_leaves.month_updated != current_date.month :
            emp_leaves.current_EL = emp_leaves.current_EL + 1.5
            emp_leaves.CasualLeave = emp_leaves.CasualLeave + 0.67
            emp_leaves.month_updated = current_date.month
        
        emp_leaves.EarnLeave = emp_leaves.Prev_CFEL + emp_leaves.current_EL 
        emp_leaves.TotalLeaves = emp_leaves.EarnLeave + emp_leaves.CasualLeave

        emp_leaves.save()
        
        context={
            'TotalLeaves': emp_leaves.TotalLeaves,
            'CasualLeave': emp_leaves.CasualLeave,
            'EarnLeave': emp_leaves.EarnLeave,
            'current_EL':emp_leaves.current_EL,
            'leave_data': leave_data
        }
        if request.user.user_type == '3':
            return render(request, "hr_management/employee_template/employee_apply_leave.html", context)
        else:
            return render(request, "hr_management/manager_template/manager_apply_leave.html", context)
    except:
        if request.user.user_type == '3':
            return render(request, "hr_management/employee_template/leave_error_msg.html")
        else:
            return render(request, "hr_management/manager_template/leave_error_msg.html")


from django.core.exceptions import ValidationError
@require_user_type(user_type=[3,4])
@login_required(login_url='do_login')
def employee_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("employee_apply_leave"))
    else:
        leave_start_dates = request.POST.getlist("leave_start_date")
        leave_end_dates = request.POST.getlist("leave_end_date")
        leave_msgs = request.POST.getlist("leave_msg")
        leave_types = request.POST.getlist("leave_type")
        employee_obj = Employees.objects.get(admin=request.user.id)
        # Check if any previous leave is still pending
        pending_leaves = LeaveReportEmployee.objects.filter(
            employee_id=employee_obj,
            leave_status=0  # 0: Pending
        )
        if pending_leaves.exists():
            messages.error(request, "You have a pending leave. Please wait for it to be approved.")
            return HttpResponseRedirect(reverse("employee_apply_leave"))
        for start_date, end_date, msg, leave_type in zip(leave_start_dates, leave_end_dates, leave_msgs, leave_types):
            try:
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                if end_date < start_date:
                    raise Exception("You cannot select an end date before the start date.")
                # Exclude Saturdays and Sundays
                leave_dates = []
                current_date = start_date
                while current_date <= end_date:
                    if current_date.weekday() < 5:
                        leave_dates.append(current_date)
                    current_date += timedelta(days=1)
                if len(leave_dates) < 1:
                    raise Exception("You are applying for a Saturday-Sunday leave.")
                existing_leave_dates = LeaveReportEmployee.objects.filter(
                    employee_id=employee_obj,
                    leave_start_date__in=leave_dates,
                    leave_end_date__in=leave_dates
                )
                conflicting_dates = []
                for leave_date in existing_leave_dates:
                    conflicting_dates.append(leave_date.leave_start_date.strftime("%Y-%m-%d"))
                if conflicting_dates:
                    raise Exception("You have already applied for leave on that day.")
                # Check if any of the leave dates are already applied
                existing_leave_dates = LeaveReportEmployee.objects.filter(
                    employee_id=employee_obj,
                    leave_start_date__lte=end_date,
                    leave_end_date__gte=start_date
                )
                for leave_date in existing_leave_dates:
                    leave_range = set(leave_dates)
                    existing_range = set(leave_date.leave_dates())
                    if leave_range.intersection(existing_range):
                        raise Exception("You have already applied for leave on that day.")
                leave_duration = len(leave_dates)
                leave_report = LeaveReportEmployee(
                    employee_id=employee_obj,
                    leave_type=leave_type,
                    leave_start_date=leave_dates[0],
                    leave_end_date=leave_dates[-1],
                    leave_message=msg,
                    leave_status=0
                )
                leave_report.full_clean()  # Validate the model data before saving
                leave_report.save()
                messages.success(request, f"Successfully applied for leave. Leave duration: {leave_duration} day(s).")
            except ValidationError as e:
                for field, error in e.message_dict.items():
                    messages.error(request, f"Validation error for field '{field}': {error[0]}")
            except Exception as e:
                messages.error(request, f"Failed to apply for leave: {str(e)}")
                return HttpResponseRedirect(reverse("employee_apply_leave") + f"?error={str(e)}")
        return HttpResponseRedirect(reverse("employee_apply_leave"))

    
# def employee_apply_leave_save(request):
#     if request.method != "POST":
#         return HttpResponseRedirect(reverse("employee_apply_leave"))
#     else:
#         leave_start_dates = request.POST.getlist("leave_start_date")
#         leave_end_dates = request.POST.getlist("leave_end_date")
#         leave_msgs = request.POST.getlist("leave_msg")
#         leave_types = request.POST.getlist("leave_type")

#         employee_obj = Employees.objects.get(admin=request.user.id)

#         for start_date, end_date, msg, leave_type in zip(leave_start_dates, leave_end_dates, leave_msgs, leave_types):
#             try:
#                 start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#                 end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

#                 # Exclude Saturdays and Sundays
#                 leave_dates = []
#                 current_date = start_date
#                 while current_date <= end_date:
#                     if current_date.weekday() < 5:  # Exclude Saturday (5) and Sunday (6)
#                         leave_dates.append(current_date)
#                     current_date += timedelta(days=1)

#                 if len(leave_dates) < 1:
#                     raise Exception("You are applying for a Saturday-Sunday leave.")

#                 existing_leave_dates = LeaveReportEmployee.objects.filter(
#                     employee_id=employee_obj,
#                     leave_start_date__in=leave_dates,
#                     leave_end_date__in=leave_dates
#                 )

#                 conflicting_dates = []
#                 for leave_date in existing_leave_dates:
#                     conflicting_dates.append(leave_date.leave_start_date.strftime("%Y-%m-%d"))
                

#                 if conflicting_dates:
#                     raise Exception("You have already applied for leave on that day.")
                

#                 # Check if any of the leave dates are already applied
#                 existing_leave_dates = LeaveReportEmployee.objects.filter(
#                     employee_id=employee_obj,
#                     leave_start_date__lte=end_date,
#                     leave_end_date__gte=start_date
#                 )
#                 for leave_date in existing_leave_dates:
#                     leave_range = set(leave_dates)
#                     existing_range = set(leave_date.get_leave_dates())
#                     if leave_range.intersection(existing_range):
#                         raise Exception("You have already applied for leave on that day.")

#                 leave_duration = len(leave_dates)

#                 leave_report = LeaveReportEmployee(
#                     employee_id=employee_obj,
#                     leave_type=leave_type,
#                     leave_start_date=leave_dates[0],
#                     leave_end_date=leave_dates[-1],
#                     leave_message=msg,
#                     leave_status=0
#                 )
#                 leave_report.full_clean()  # Validate the model data before saving
#                 leave_report.save()
#                 messages.success(request, f"Successfully Applied for Leave. Leave duration: {leave_duration} day(s).")
#             except ValidationError as e:
#                 for field, error in e.message_dict.items():
#                     messages.error(request, f"Validation error for field '{field}': {error[0]}")
#             except Exception as e:
#                 messages.error(request, f"Failed to apply for leave: {str(e)}")
#                 return HttpResponseRedirect(reverse("employee_apply_leave") + f"?error={str(e)}")

#         return HttpResponseRedirect(reverse("employee_apply_leave"))

#working middle only msg change i want

# def employee_apply_leave_save(request):
#     if request.method != "POST":
#         return HttpResponseRedirect(reverse("employee_apply_leave"))
#     else:
#         leave_start_dates = request.POST.getlist("leave_start_date")
#         leave_end_dates = request.POST.getlist("leave_end_date")
#         leave_msgs = request.POST.getlist("leave_msg")
#         leave_types = request.POST.getlist("leave_type")

#         employee_obj = Employees.objects.get(admin=request.user.id)

#         for start_date, end_date, msg, leave_type in zip(leave_start_dates, leave_end_dates, leave_msgs, leave_types):
#             try:
#                 start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
#                 end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

#                 # Exclude Saturdays and Sundays
#                 leave_dates = []
#                 current_date = start_date
#                 while current_date <= end_date:
#                     if current_date.weekday() < 5:  # Exclude Saturday (5) and Sunday (6)
#                         leave_dates.append(current_date)
#                     current_date += datetime.timedelta(days=1)

#                 if len(leave_dates) < 1:
#                     raise Exception("You are applying for a Saturday-Sunday leave.")

#                 existing_leave_dates = LeaveReportEmployee.objects.filter(
#                     employee_id=employee_obj,
#                     leave_start_date__lte=end_date,
#                     leave_end_date__gte=start_date
#                 )

#                 conflicting_dates = []
#                 for leave_date in existing_leave_dates:
#                     leave_range = set(
#                         datetime.datetime.strftime(date, "%Y-%m-%d")
#                         for date in pd.date_range(leave_date.leave_start_date, leave_date.leave_end_date + datetime.timedelta(days=1))
#                     )
#                     if any(date in leave_range for date in leave_dates):
#                         conflicting_dates.append(
#                             leave_date.leave_start_date.strftime("%Y-%m-%d") + " to " +
#                             leave_date.leave_end_date.strftime("%Y-%m-%d")
#                         )

#                 if conflicting_dates:
#                     raise Exception(f"You have already applied for leave on the following day(s): {', '.join(conflicting_dates)}")

#                 leave_duration = len(leave_dates)

#                 leave_report = LeaveReportEmployee(
#                     employee_id=employee_obj,
#                     leave_type=leave_type,
#                     leave_start_date=leave_dates[0],
#                     leave_end_date=leave_dates[-1],
#                     leave_message=msg,
#                     leave_status=0
#                 )
#                 leave_report.full_clean()  # Validate the model data before saving
#                 leave_report.save()
#                 messages.success(request, f"Successfully Applied for Leave. Leave duration: {leave_duration} day(s).")
#             except ValidationError as e:
#                 for field, error in e.message_dict.items():
#                     messages.error(request, f"Validation error for field '{field}': {error[0]}")
#             except Exception as e:
#                 messages.error(request, f"Failed to apply for leave: {str(e)}")
#                 return HttpResponseRedirect(reverse("employee_apply_leave") + f"?error={str(e)}")

#         return HttpResponseRedirect(reverse("employee_apply_leave"))

# def employee_apply_leave_save(request):
#     if request.method != "POST":
#         return HttpResponseRedirect(reverse("employee_apply_leave"))
#     else:
#         leave_start_dates = request.POST.getlist("leave_start_date")
#         leave_end_dates = request.POST.getlist("leave_end_date")
#         leave_msgs = request.POST.getlist("leave_msg")
#         leave_types = request.POST.getlist("leave_type")

#         employee_obj = Employees.objects.get(admin=request.user.id)

#         for start_date, end_date, msg, leave_type in zip(leave_start_dates, leave_end_dates, leave_msgs, leave_types):
#             try:
#                 start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
#                 end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

#                 # Exclude Saturdays and Sundays
#                 leave_dates = []
#                 current_date = start_date
#                 while current_date <= end_date:
#                     if current_date.weekday() < 5:  # Exclude Saturday (5) and Sunday (6)
#                         leave_dates.append(current_date)
#                     current_date += datetime.timedelta(days=1)

#                 if len(leave_dates) < 1:
#                     raise Exception("You are applying for a Saturday-Sunday leave.")

#                 existing_leave_dates = LeaveReportEmployee.objects.filter(
#                     employee_id=employee_obj,
#                     leave_start_date__lte=end_date,
#                     leave_end_date__gte=start_date
#                 )

#                 conflicting_dates = []
#                 for leave_date in existing_leave_dates:
#                     leave_range = [
#                         date.strftime("%Y-%m-%d")
#                         for date in pd.date_range(leave_date.leave_start_date, leave_date.leave_end_date + datetime.timedelta(days=1))
#                     ]
#                     conflicting_dates += list(set(leave_range) & set(leave_dates))

#                 if conflicting_dates:
#                     conflicting_dates_str = ", ".join(conflicting_dates)
#                     raise Exception(f"You have already applied for leave on the following day(s): {conflicting_dates_str}")

#                 leave_duration = len(leave_dates)

#                 leave_report = LeaveReportEmployee(
#                     employee_id=employee_obj,
#                     leave_type=leave_type,
#                     leave_start_date=leave_dates[0],
#                     leave_end_date=leave_dates[-1],
#                     leave_message=msg,
#                     leave_status=0
#                 )
#                 leave_report.full_clean()  # Validate the model data before saving
#                 leave_report.save()
#                 messages.success(request, f"Successfully Applied for Leave. Leave duration: {leave_duration} day(s).")
#             except ValidationError as e:
#                 for field, error in e.message_dict.items():
#                     messages.error(request, f"Validation error for field '{field}': {error[0]}")
#             except Exception as e:
#                 messages.error(request, f"Failed to apply for leave: {str(e)}")
#                 # Handle the custom message here instead of returning HttpResponseRedirect
#                 # You can redirect to the appropriate page or show the message on the current page
#                 messages.info(request, str(e))

#         return HttpResponseRedirect(reverse("employee_apply_leave"))

@require_user_type(user_type=3)
@login_required(login_url='do_login')
def employee_feedback(request):
    employee_id_id=Employees.objects.get(admin=request.user.id)
    feedback_data=FeedBackEmployee.objects.filter(employee_id=employee_id_id)
    return render(request,"hr_management/employee_template/employee_feedback.html",{"feedback_data":feedback_data})


@require_user_type(user_type=3)
@login_required(login_url='do_login')
def employee_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("employee_feedback"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        employee_obj=Employees.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackEmployee(employee_id=employee_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("employee_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("employee_feedback"))


@require_user_type(user_type=3)
@login_required(login_url='do_login')
def employee_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    employee=Employees.objects.get(admin=user)
    return render(request,"hr_management/employee_template/employee_profile.html",{"user":user,"employee":employee})


@require_user_type(user_type=3)
@login_required(login_url='do_login')
def employee_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("employee_profile"))
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

            employee=Employees.objects.get(admin=customuser)
            employee.profile_pic=profile_pic
            employee.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("employee_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("employee_profile"))


@require_user_type(user_type=3)
@login_required(login_url='do_login')
@csrf_exempt
def employee_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        employee=Employees.objects.get(admin=request.user.id)
        employee.fcm_token=token
        employee.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@require_user_type(user_type=3)
@login_required(login_url='do_login')
def employee_all_notification(request):
    employee_id = request.user.id
    notifications = NotificationEmployee.objects.filter(employee_id=employee_id)
    print(notifications, 'nnnn')
    return render(request, "hr_management/employee_template/all_notification.html", {"notifications": notifications})


@require_user_type(user_type=[3,4])
@login_required(login_url='do_login')
def EmployeeOnboarding(request, pk=None):
    employee = Employees.objects.get(admin=request.user)
    emp_address_form = EmployeeAddressDetailsFrom()
    emp_perment_address_form = EmployeePermentAddressFrom()
    emp_family_form = FamilyDetailsForm()
    emp_bank_form = BankDetailsForm()
    emp_document_form = DocumentsForm()

    onboarding_status = Employee_Onboarding.objects.filter(employee=employee).exists()
    if onboarding_status:
            if request.user.user_type == '3':
                return render(request,'hr_management/employee_template/onboarding_completed_msg.html')
            else:
                return render(request,'hr_management/manager_template/onboarding_completed_msg.html')

    if request.method == 'POST':
        onboarding_form = EmployeeOnboardingForm(request.POST)
        address_form = EmployeeAddressDetailsFrom(request.POST)
        perment_address_form = EmployeePermentAddressFrom(request.POST)
        family_form = FamilyDetailsForm(request.POST)
        bank_form = BankDetailsForm(request.POST)
        document_form = DocumentsForm(request.POST, request.FILES)
        current_date = datetime.datetime.now().date()
        emp_data = EmployeeLeave.objects.filter(employee_id=employee).first()
        TotalLeaves = 0
        CasualLeave = 0
        current_EL = 0
        month_updated = current_date.month
        
        
        emp_data = EmployeeLeave.objects.create(
                employee_id=employee,
                TotalLeaves=TotalLeaves,
                CasualLeave=CasualLeave,
                current_EL=current_EL,
                EarnLeave=current_EL,
                month_updated=month_updated
            )
        emp_data.save()
        
        latest_emp = EmployeeLeave.objects.latest('id')       
                 
        latest_emp.save()

        if onboarding_form.is_valid() and address_form.is_valid() and perment_address_form.is_valid() and family_form.is_valid() and bank_form.is_valid() and document_form.is_valid():

            address = address_form.save(commit=False)
            perment_address = perment_address_form.save(commit=False)
            address.employee = employee
            address.save()

            perment_address.employee = employee
            perment_address.save()

            onboarding_form.instance.employee = employee
            onboarding_form.save()

            family_form.instance.employee = employee
            family_form.save()

            bank_form.instance.employee = employee
            bank_form.save()

            document_form.instance.employee = employee
            document = document_form.save(commit=False)
            document.employee = employee
            document.save()
            return redirect('all_records')

    else:
        address_form = EmployeeAddressDetailsFrom()
        perment_address_form = EmployeePermentAddressFrom()
        family_form = FamilyDetailsForm()
        bank_form = BankDetailsForm()
        document_form = DocumentsForm()
        onboarding_form = EmployeeOnboardingForm()
    if request.user.user_type == '3':
        return render(request, 'hr_management/employee_template/employee_onboarding.html', {'emp_onboarding_form': onboarding_form, 'emp_address_form': emp_address_form, 'emp_perment_address_form': emp_perment_address_form, 'emp_family_form': emp_family_form, 'emp_bank_form': emp_bank_form, 'emp_document_form': emp_document_form})
    else:
        return render(request, 'hr_management/manager_template/manager_onboarding.html', {'emp_onboarding_form': onboarding_form, 'emp_address_form': emp_address_form, 'emp_perment_address_form': emp_perment_address_form, 'emp_family_form': emp_family_form, 'emp_bank_form': emp_bank_form, 'emp_document_form': emp_document_form})
        

@require_user_type(user_type=[3,4])
@login_required(login_url='do_login')
def AllRecords(request):
    user=CustomUser.objects.get(id=request.user.id)
    employee=Employees.objects.get(admin=user)
    personal_info = Employee_Onboarding.objects.filter(employee=employee)
    current_address = Address_detail.objects.filter(employee=employee)
    per_address = Permanent_Address.objects.filter(employee=employee)
    emp_family_details = FamilyDetails.objects.filter(employee=employee)
    bank_details =BankDetails.objects.filter(employee=employee)
    documents = Documents.objects.filter(employee=employee)
    context = {'personal_info': personal_info, 'current_address': current_address, 'per_address':per_address,'emp_family_details':emp_family_details,'bank_details':bank_details,'documents': documents} 
    if request.user.user_type == '3':
        template_name = 'hr_management/employee_template/records.html'
        return render(request, template_name, context)
    else:
        template_name = 'hr_management/manager_template/records.html'
        return render(request, template_name, context)
        


@require_user_type(user_type=[3,4])
@login_required(login_url='do_login')
def employee_salary_view(request):
    employee = get_object_or_404(Employees, admin=request.user)
    salary_slips = SalarySlip.objects.filter(employee_id=employee)
    if not salary_slips:
            if request.user.user_type == '3':
                return render(request,'hr_management/employee_template/salary_slip_not_generated.html')
            else:
                return render(request,'hr_management/manager_template/salary_slip_not_generated.html')

    unique_months = set()
    unique_years = set()
    for salary in salary_slips:
        unique_months.add(salary.month)
        unique_years.add(salary.year)
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        if selected_month:
            salary_slips = salary_slips.filter(month=selected_month)
        if selected_year:
            salary_slips = salary_slips.filter(year=selected_year)
        selected_salary_slip = salary_slips.first()
 
        if not selected_salary_slip:
            return render(request,'hr_management/employee_template/salary_slip_not_generated.html')

        month_short = selected_salary_slip.month[0:3]
        year_short = selected_salary_slip.year[2:4]
        number2word = num2words(selected_salary_slip.net_salary)
        capitalized_word = number2word.title()
        bank_details = BankDetails.objects.filter(employee=employee).first()
        bank_name = bank_details.bank_name if bank_details else None
        account_number = bank_details.account_number if bank_details else None
        onboarding_data = Employee_Onboarding.objects.filter(employee_id=employee)
        if request.user.user_type == '3':
            return render(request, "hr_management/employee_template/salary.html", {
                "salary_slips": salary_slips,
                "salary_slip": selected_salary_slip,
                "selected_salary_slip": selected_salary_slip,
                "employee": employee,
                "onboarding_data": onboarding_data,
                "capitalized_word": capitalized_word,
                "account_number": account_number,
                "bank_name": bank_name,
                "month_short": month_short,
                "year_short": year_short
            })
        else:
                return render(request, "hr_management/manager_template/salary.html", {
                "salary_slips": salary_slips,
                "salary_slip": selected_salary_slip,
                "selected_salary_slip": selected_salary_slip,
                "employee": employee,
                "onboarding_data": onboarding_data,
                "capitalized_word": capitalized_word,
                "account_number": account_number,
                "bank_name": bank_name,
                "month_short": month_short,
                "year_short": year_short
            })
    if request.user.user_type == '3':
        return render(request, "hr_management/employee_template/salary.html",{'unique_months':unique_months,'unique_years':unique_years})
    else:
        return render(request, "hr_management/manager_template/salary.html",{'unique_months':unique_months,'unique_years':unique_years})
