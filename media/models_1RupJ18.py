from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


class CustomUser(AbstractUser):
    user_type_data=((1,"Admin"),(2,"HR"),(3,"Employee"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)
    email = models.EmailField(unique=True)
    

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class HRs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()


# class Employees(models.Model):
#     id=models.AutoField(primary_key=True)
#     emp_id = models.BigIntegerField(null=True, blank=True)
#     admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
#     gender=models.CharField(max_length=255)
#     profile_pic=models.FileField()
#     address=models.TextField() 
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now_add=True)
#     fcm_token=models.TextField(default="")
#     objects = models.Manager()


# from django.contrib.auth.models import User

# class Employees(models.Model):
#     id = models.AutoField(primary_key=True)
#     emp_id = models.CharField(max_length=10, null=True, blank=True, unique=True)
#     admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     gender = models.CharField(max_length=255)
#     profile_pic = models.FileField()
#     address = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     fcm_token = models.TextField(default="")

#     objects = models.Manager()

#     @staticmethod
#     def generate_emp_id():
#         last_emp = Employees.objects.order_by('-id').first()  # Get the last employee
#         last_emp_id = last_emp.emp_id if last_emp else 'OTS_10000'

#         if last_emp_id:
#             emp_num = int(last_emp_id.split('_')[1]) + 1
#         else:
#             emp_num = 10000

#         emp_id = f'OTS_{emp_num:05d}'  # Generate emp_id in the format OTS_XXXXX
#         return emp_id


class Employees(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=25, blank=True)

    def save(self, *args, **kwargs):
        # set the emp_id field to the next available ID in the format OTS_XXXXX
        if not self.emp_id:
            last_emp = Employees.objects.order_by('-id').first()
            if last_emp:
                last_number = int(last_emp.emp_id.split('_')[1])
            else:
                last_number = 10000  # Start with 10000 if no previous employee exists
            self.emp_id = 'OTS_{:05d}'.format(last_number + 1)
        super(Employees, self).save(*args, **kwargs)

    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255)
    profile_pic = models.FileField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    fcm_token = models.TextField(default="")

    objects = models.Manager()

################################# On Boarding ############################################
class Employee_Onboarding(models.Model):
    MARITAL_STATUS=(
        ('married','Married'),
        ('unmarried','Unmarried')
    )
    Gender = (
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
    )
    employee=models.OneToOneField(Employees,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_no= models.CharField(max_length=10)
    emergency_contact_no = models.CharField(max_length=10)
    pancard_no= models.CharField(max_length=10)
    adhaar_no= models.CharField(max_length=12) 
    pf_uan_no = models.CharField(max_length=30)
    blood_group = models.CharField(max_length=20)
    dob = models.DateField()
    gender = models.CharField(max_length=20,choices=Gender)
    marital_status = models.CharField(max_length=30, choices=MARITAL_STATUS)
    highest_qualification = models.CharField(max_length=50)
    previous_company_name = models.CharField(max_length=30)
    date_of_joining = models.DateField()



class Address_detail(models.Model):
    ADDRESS_TYPES = (
        ('current', 'Current Address'),
        ('permanent', 'Permanent Address'),
        ('other', 'Other Address'),
    )
    employee=models.OneToOneField(Employees,on_delete=models.CASCADE)
    add_type = models.CharField(max_length=30, choices=ADDRESS_TYPES, default='current')
    address1 = models.CharField(max_length=1024)
    address2 = models.CharField(max_length=1024)
    zip_code = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    dist = models.CharField(max_length=100)
    state = models.CharField(max_length=100,default='Maharashtra')
    country = models.CharField(max_length=30)
    
    def __str__(self):
        return f'{self.employee}'

class Permanent_Address(models.Model):
    ADDRESS_TYPES = (
        ('current', 'Current Address'),
        ('permanent', 'Permanent Address'),
        ('other', 'Other Address'),
    )
    employee=models.OneToOneField(Employees,on_delete=models.CASCADE)
    per_add_type = models.CharField(max_length=30, choices=ADDRESS_TYPES, default='perment')
    per_address1 = models.CharField(max_length=200)
    per_address2 = models.CharField(max_length=200)
    per_zip_code = models.CharField(max_length=6)
    per_city = models.CharField(max_length=100)
    per_dist = models.CharField(max_length=100)
    per_state = models.CharField(max_length=100,default='Maharashtra')
    per_country = models.CharField(max_length=30)
    def __str__(self):
        return f'{self.employee}'


class FamilyDetails(models.Model):
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE)
    member1_name = models.CharField(max_length=50)
    merber1_dob = models.DateField()
    merber1_aadhar_no = models.CharField(max_length=12)
    relationship1 = models.CharField(max_length=50)
    member2_name = models.CharField(max_length=50)
    merber2_dob = models.DateField()
    merber2_aadhar_no = models.CharField(max_length=12)
    relationship2 = models.CharField(max_length=50)
    member3_name = models.CharField(max_length=50)
    merber3_dob = models.DateField()
    merber3_aadhar_no = models.CharField(max_length=12)
    relationship3 = models.CharField(max_length=50)
    member4_name = models.CharField(max_length=50, blank=True, null=True)
    merber4_dob = models.DateField(null=True, blank=True)
    merber4_aadhar_no = models.CharField(max_length=12, blank=True, null=True)
    relationship4 = models.CharField(max_length=50, blank=True, null=True)
    member5_name = models.CharField(max_length=50, blank=True, null=True)
    merber5_dob = models.DateField(null=True, blank=True)
    merber5_aadhar_no = models.CharField(max_length=12, blank=True, null=True)
    relationship5 = models.CharField(max_length=50, blank=True, null=True)



class BankDetails(models.Model):
    employee=models.OneToOneField(Employees,on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    account_number = models.CharField(max_length=20)
    ifsc_number = models.CharField(max_length=20)


def get_upload_to(instance, filename):
    return "pdfs/employee_{id}/{filename}".format(id=instance.employee.id, filename=filename)

class Documents(models.Model):
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE)
    employee_photo = models.FileField(upload_to=get_upload_to)
    employee_aadhar = models.FileField(upload_to=get_upload_to)
    employee_pan = models.FileField(upload_to=get_upload_to)
    ssc_marksheet = models.FileField(upload_to=get_upload_to)
    hsc_marksheet = models.FileField(upload_to=get_upload_to)
    diploma_marksheet = models.FileField(upload_to=get_upload_to)
    degree_marksheet = models.FileField(upload_to=get_upload_to)
    bank_passbook = models.FileField(upload_to=get_upload_to)
    passport = models.FileField(upload_to=get_upload_to)
    reliving_letter = models.FileField(upload_to=get_upload_to)
    family_member1_aadhar = models.FileField(upload_to=get_upload_to)
    family_member2_aadhar = models.FileField(upload_to=get_upload_to)
    family_member3_aadhar = models.FileField(upload_to=get_upload_to)
    family_member4_aadhar = models.FileField(upload_to=get_upload_to, null=True, blank=True)
    family_member5_aadhar = models.FileField(upload_to=get_upload_to, null=True, blank=True)


# class EmployeePayroll(models.Model):
#     employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
#     basic_salary = models.FloatField()
#     hra = models.FloatField()
#     conveyance_allowance = models.FloatField()
#     flexible_component = models.FloatField()
#     variable_component = models.FloatField()
#     provident_fund  = models.FloatField()
#     esic = models.FloatField()
#     professional_tax = models.FloatField()
#     income_tax = models.FloatField()
#     other_deductions = models.FloatField() 
#     month = models.DateField()
#     salary = models.FloatField()
#     bonus = models.FloatField()
#     total = models.FloatField()

#     def __str__(self):
#         return f"{self.employee} - {self.month.strftime('%b, %Y')}"

import calendar
class EmployeePayroll(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    month = models.DateField()
    year = models.IntegerField(null=True)
    ctc = models.DecimalField(max_digits=20, decimal_places=2)
    working_days = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    hra = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    conveyance_allowance = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    flexible_component = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    bonus = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    provident_fund = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    esic = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    professional_tax = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    income_tax = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    other_deductions = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    salary = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    gross_salary = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_deductions = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    net_salary = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.employee} - {self.month.strftime('%b %Y')}"


    def get_working_days(self):
        year = self.year
        month = self.month.month
        days_in_month = calendar.monthrange(year, month)[1]
        return days_in_month
    


# class Attendance(models.Model):
#     id=models.AutoField(primary_key=True)
#     attendance_date=models.DateField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now_add=True)
#     objects = models.Manager()

# class AttendanceReport(models.Model):
#     id=models.AutoField(primary_key=True)
#     employee_id=models.ForeignKey(Employees,on_delete=models.DO_NOTHING)
#     attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
#     status=models.BooleanField(default=False)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now_add=True)
#     objects=models.Manager()

class LeaveReportEmployee(models.Model):
    id=models.AutoField(primary_key=True)
    employee_id=models.ForeignKey(Employees,on_delete=models.CASCADE)
    leave_date=models.DateTimeField(max_length=255, null=True,blank=True)
    leave_message=models.TextField()
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    leave_type=models.CharField(max_length=100)
    leave_start_date = models.DateField(max_length=255)
    leave_end_date = models.DateField(max_length=255)


    
      
# class EmployeeLeave(models.Model):
#     id=models.AutoField(primary_key=True)
#     employee_id=models.ForeignKey(Employees,on_delete=models.CASCADE)
#     EarnLeave =models.FloatField(default=0)
#     CasualLeave =models.FloatField(default=0)
#     TotalLeaves = models.FloatField(default=0)
#     EarnLeave_used =models.FloatField(default=0)
#     CasualLeave_used =models.FloatField(default=0)
#     remaining_leaves=models.FloatField(default=0)
#     total_leaves_taken=models.FloatField(default=0)
#     new_leave=models.FloatField(default=0)
#     year_updated = models.IntegerField(default=0)

     
class EmployeeLeave(models.Model):
    id=models.AutoField(primary_key=True)
    employee_id=models.ForeignKey(Employees,on_delete=models.CASCADE)
    EarnLeave =models.FloatField(default=0)
    CasualLeave =models.FloatField(default=0)
    TotalLeaves = models.FloatField(default=0)
    EarnLeave_used =models.FloatField(default=0)
    CasualLeave_used =models.FloatField(default=0)
    # remaining_leaves=models.FloatField(default=0)
    # total_leaves_taken=models.FloatField(default=0)
    # new_leave=models.FloatField(default=0)
    month_updated = models.IntegerField(default=0)
    year_updated = models.IntegerField(default=0)
    Prev_CFEL = models.FloatField(default=0)
    current_EL = models.FloatField(default=0)
    # prev_ref_date =  models.DateField()

    # cur_EL = models.FloatField(default=0)
    # EarnLeave_total = models.IntegerField(default=0)
    # CasualLeave_total = models.IntegerField(default=0) 
    
# class EmployeeLeave(models.Model):
    # id=models.AutoField(primary_key=True)
    # employee_id=models.ForeignKey(LeaveReportEmployee,on_delete=models.CASCADE)
    # EarnLeave =models.FloatField(default=0)
    # CasualLeave =models.FloatField(default=0)
    # TotalLeaves = models.FloatField(default=0)
    # EarnLeave_used =models.FloatField(default=0)
    # CasualLeave_used =models.FloatField(default=0)
    # remaining_leaves=models.FloatField(default=0)
    # total_leaves_taken=models.FloatField(default=0)
    # new_leave=models.FloatField(default=0)
    

class LeaveReportHR(models.Model):
    id = models.AutoField(primary_key=True)
    hr_id = models.ForeignKey(HRs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackHRs(models.Model):
    id = models.AutoField(primary_key=True)
    hr_id = models.ForeignKey(HRs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationHRs(models.Model):
    id = models.AutoField(primary_key=True)
    hr_id = models.ForeignKey(HRs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()




@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            HRs.objects.create(admin=instance,address="")
        if instance.user_type==3:
            Employees.objects.create(admin=instance,address="",profile_pic="",gender="")



@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.hrs.save()
    if instance.user_type==3:
        instance.employees.save()



######################### OFFER LETTER ########################################
class OfferLetter(models.Model):
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    total_fixed_pay = models.DecimalField(max_digits=10, decimal_places=2)
    total_variable_pay = models.DecimalField(max_digits=10, decimal_places=2)
    insurance_premiums = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost_to_company = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    esic = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    employer_pf_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    flexible_components_tfp = models.DecimalField(max_digits=10, decimal_places=2)

class OfferLetter_Sended(models.Model):
    offerletter = models.ManyToManyField(OfferLetter)
    ctc = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    offer_release_date = models.DateField(blank=True, null=True)
    joining_date = models.DateField()
    address = models.CharField(max_length=100)
    designation = models.CharField(max_length=50)
    job_grade = models.IntegerField()
    reporting = models.CharField(max_length=50)
    hr_name = models.CharField(max_length=50)
    offer_accept_date = models.DateField()
    def __str__(self):
        return self.name


class SalarySlip(models.Model):
    # employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    ctc = models.DecimalField(max_digits=10, decimal_places=2)
    # name = models.CharField(max_length=100, blank=True, null=True)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    flexible_component = models.DecimalField(max_digits=10, decimal_places=2)
    variable_component= models.DecimalField(max_digits=10, decimal_places=2)
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2)
    esic = models.DecimalField(max_digits=10, decimal_places=2)
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2)
    income_tax = models.DecimalField(max_digits=10, decimal_places=2)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    days_payable = models.IntegerField()
    

