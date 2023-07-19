from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_type_data=((1,"Admin"),(2,"HR"),(3,"Employee"),((4,"Manager")))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)
    email = models.EmailField(unique=True)
    manager = models.CharField(max_length=150)

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class HRs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    department = models.CharField(max_length=50, default='')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()


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
    manager = models.CharField(max_length=50)
    department = models.CharField(max_length=50, default='')
    designation = models.CharField(max_length=50, default='')
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
    employee_photo = models.FileField(upload_to=get_upload_to, blank=True, null=True)
    employee_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    employee_pan = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    ssc_marksheet = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    hsc_marksheet = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    diploma_marksheet = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    degree_marksheet = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    bank_passbook = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    passport = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    reliving_letter = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    family_member1_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    family_member2_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    family_member3_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    family_member4_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    family_member5_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)



from datetime import timedelta
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
    def leave_dates(self):
        return [self.leave_start_date + timedelta(days=i) for i in range((self.leave_end_date - self.leave_start_date).days + 1)]


class EmployeeLeave(models.Model):
    id=models.AutoField(primary_key=True)
    employee_id=models.ForeignKey(Employees,on_delete=models.CASCADE)
    EarnLeave =models.FloatField(default=0)
    CasualLeave =models.FloatField(default=0)
    TotalLeaves = models.FloatField(default=0)
    EarnLeave_used =models.FloatField(default=0)
    CasualLeave_used =models.FloatField(default=0)
    month_updated = models.IntegerField(default=0)
    year_updated = models.IntegerField(default=0)
    Prev_CFEL = models.FloatField(default=0)
    current_EL = models.FloatField(default=0)



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
        elif instance.user_type==2:
            HRs.objects.create(admin=instance)
        elif instance.user_type==3 or instance.user_type==4:
            Employees.objects.create(admin=instance)
        # elif instance.user_type==4:
        #     Employees.objects.create(admin=instance,gender="")


@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    elif instance.user_type==2:
        instance.hrs.save()
    elif instance.user_type == 3 or instance.user_type == 4:
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
    offerletter = models.OneToOneField(OfferLetter,on_delete=models.CASCADE)
    ctc = models.FloatField()
    name = models.CharField(max_length=100)
    offer_release_date = models.DateField()
    joining_date = models.DateField()
    address = models.CharField(max_length=100)
    designation = models.CharField(max_length=50)
    job_grade = models.IntegerField()
    reporting = models.CharField(max_length=50)
    hr_name = models.CharField(max_length=50)
    offer_accept_date = models.DateField()
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=10, unique=True)

    


class WageRegister(models.Model):
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='wage_registers')
    ctc = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    esic = models.DecimalField(max_digits=10, decimal_places=2)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    flexible_component = models.DecimalField(max_digits=10, decimal_places=2)
    variable_component = models.DecimalField(max_digits=10, decimal_places=2)
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2)
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2)
    income_tax = models.DecimalField(max_digits=10, decimal_places=2,default='00')
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    other_allowns = models.DecimalField(max_digits=10,decimal_places=2,default='00')
    lwf = models.DecimalField(max_digits=10,decimal_places=2,default='00')

    

    # YTD fields
    ytd_ctc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_esic = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_flexible_component = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_variable_component = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_provident_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_professional_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_income_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Additional fields
    days_payable = models.IntegerField()
    days_paid = models.IntegerField(null=True)
    address = models.CharField(max_length=500, default='')
    month = models.CharField(max_length=30, default='')
    year = models.CharField(max_length=30, default='') 
    age = models.CharField(max_length=20,default='') 



class SalarySlip(models.Model):
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='salary_slips')
    ctc = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    esic = models.DecimalField(max_digits=10, decimal_places=2)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    flexible_component = models.DecimalField(max_digits=10, decimal_places=2)
    variable_component = models.DecimalField(max_digits=10, decimal_places=2)
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2)
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2)
    income_tax = models.DecimalField(max_digits=10, decimal_places=2,default='00')
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    other_allowns = models.DecimalField(max_digits=10,decimal_places=2,default='00')
    lwf = models.DecimalField(max_digits=10,decimal_places=2,default='00')

    

    # YTD fields
    ytd_ctc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_esic = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_flexible_component = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_variable_component = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_provident_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_professional_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_income_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Additional fields
    days_payable = models.IntegerField()
    days_paid = models.IntegerField(null=True)
    address = models.CharField(max_length=500, default='')
    month = models.CharField(max_length=30, default='')
    year = models.CharField(max_length=30, default='')















# class Manager_Onboarding(models.Model):
#     MARITAL_STATUS=(
#         ('married','Married'),
#         ('unmarried','Unmarried')
#     )
#     Gender = (
#         ('male','Male'),
#         ('female','Female'),
#         ('other','Other')
#     )
#     manager=models.OneToOneField(Managers,on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     contact_no= models.CharField(max_length=10)
#     emergency_contact_no = models.CharField(max_length=10)
#     pancard_no= models.CharField(max_length=10)
#     adhaar_no= models.CharField(max_length=12) 
#     pf_uan_no = models.CharField(max_length=30)
#     blood_group = models.CharField(max_length=20)
#     dob = models.DateField()
#     gender = models.CharField(max_length=20,choices=Gender)
#     marital_status = models.CharField(max_length=30, choices=MARITAL_STATUS)
#     highest_qualification = models.CharField(max_length=50)
#     previous_company_name = models.CharField(max_length=30)
#     date_of_joining = models.DateField()

# class ManagerAddress_detail(models.Model):
#     ADDRESS_TYPES = (
#         ('current', 'Current Address'),
#         ('permanent', 'Permanent Address'),
#         ('other', 'Other Address'),
#     )
#     manager=models.OneToOneField(Managers,on_delete=models.CASCADE)
#     add_type = models.CharField(max_length=30, choices=ADDRESS_TYPES, default='current')
#     address1 = models.CharField(max_length=1024)
#     address2 = models.CharField(max_length=1024)
#     zip_code = models.CharField(max_length=6)
#     city = models.CharField(max_length=100)
#     dist = models.CharField(max_length=100)
#     state = models.CharField(max_length=100,default='Maharashtra')
#     country = models.CharField(max_length=30)
    
#     def __str__(self):
#         return f'{self.employee}'

# class ManagerPermanent_Address(models.Model):
#     ADDRESS_TYPES = (
#         ('current', 'Current Address'),
#         ('permanent', 'Permanent Address'),
#         ('other', 'Other Address'),
#     )
#     manager=models.OneToOneField(Managers,on_delete=models.CASCADE)
#     per_add_type = models.CharField(max_length=30, choices=ADDRESS_TYPES, default='perment')
#     per_address1 = models.CharField(max_length=200)
#     per_address2 = models.CharField(max_length=200)
#     per_zip_code = models.CharField(max_length=6)
#     per_city = models.CharField(max_length=100)
#     per_dist = models.CharField(max_length=100)
#     per_state = models.CharField(max_length=100,default='Maharashtra')
#     per_country = models.CharField(max_length=30)
#     def __str__(self):
#         return f'{self.employee}'


# class ManagerFamilyDetails(models.Model):
#     manager = models.OneToOneField(Managers, on_delete=models.CASCADE)
#     member1_name = models.CharField(max_length=50)
#     merber1_dob = models.DateField()
#     merber1_aadhar_no = models.CharField(max_length=12)
#     relationship1 = models.CharField(max_length=50)
#     member2_name = models.CharField(max_length=50)
#     merber2_dob = models.DateField()
#     merber2_aadhar_no = models.CharField(max_length=12)
#     relationship2 = models.CharField(max_length=50)
#     member3_name = models.CharField(max_length=50)
#     merber3_dob = models.DateField()
#     merber3_aadhar_no = models.CharField(max_length=12)
#     relationship3 = models.CharField(max_length=50)
#     member4_name = models.CharField(max_length=50, blank=True, null=True)
#     merber4_dob = models.DateField(null=True, blank=True)
#     merber4_aadhar_no = models.CharField(max_length=12, blank=True, null=True)
#     relationship4 = models.CharField(max_length=50, blank=True, null=True)
#     member5_name = models.CharField(max_length=50, blank=True, null=True)
#     merber5_dob = models.DateField(null=True, blank=True)
#     merber5_aadhar_no = models.CharField(max_length=12, blank=True, null=True)
#     relationship5 = models.CharField(max_length=50, blank=True, null=True)


# class ManagerBankDetails(models.Model):
#     manager=models.OneToOneField(Managers,on_delete=models.CASCADE)
#     bank_name = models.CharField(max_length=50)
#     branch = models.CharField(max_length=50)
#     account_number = models.CharField(max_length=20)
#     ifsc_number = models.CharField(max_length=20)


# def get_upload_to(instance, filename):
#     return "pdfs/manager_{id}/{filename}".format(id=instance.manager.id, filename=filename)

# class ManagerDocuments(models.Model):
#     manager = models.OneToOneField(Managers, on_delete=models.CASCADE)
#     manager_photo = models.FileField(upload_to=get_upload_to, blank=True, null=True)
#     manager_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)
#     manager_pan = models.FileField(upload_to=get_upload_to,blank=True, null=True)
#     ssc_marksheet = models.FileField(upload_to=get_upload_to,blank=True, null=True)
#     hsc_marksheet = models.FileField(upload_to=get_upload_to,blank=True, null=True)
#     diploma_marksheet = models.FileField(upload_to=get_upload_to,blank=True, null=True)
#     degree_marksheet = models.FileField(upload_to=get_upload_to,blank=True, null=True)
#     bank_passbook = models.FileField(upload_to=get_upload_to,blank=True, null=True)
#     passport = models.FileField(upload_to=get_upload_to,blank=True, null=True)
#     reliving_letter = models.FileField(upload_to=get_upload_to,blank=True, null=True)
#     family_member1_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)
#     family_member2_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)
#     family_member3_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)
#     family_member4_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)
#     family_member5_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)


# class ManagerLeave(models.Model):
#     id=models.AutoField(primary_key=True)
#     manager_id=models.ForeignKey(Managers,on_delete=models.CASCADE)
#     EarnLeave =models.FloatField(default=0)
#     CasualLeave =models.FloatField(default=0)
#     TotalLeaves = models.FloatField(default=0)
#     EarnLeave_used =models.FloatField(default=0)
#     CasualLeave_used =models.FloatField(default=0)
#     month_updated = models.IntegerField(default=0)
#     year_updated = models.IntegerField(default=0)
#     Prev_CFEL = models.FloatField(default=0)
#     current_EL = models.FloatField(default=0)