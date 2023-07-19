# Generated by Django 4.2 on 2023-07-18 10:24

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import hr_management_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[(1, 'Admin'), (2, 'HR'), (3, 'Employee'), (4, 'Manager')], default=1, max_length=10)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('manager', models.CharField(max_length=150)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('emp_id', models.CharField(blank=True, max_length=25)),
                ('manager', models.CharField(max_length=50)),
                ('department', models.CharField(default='', max_length=50)),
                ('designation', models.CharField(default='', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('fcm_token', models.TextField(default='')),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HRs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('department', models.CharField(default='', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('fcm_token', models.TextField(default='')),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OfferLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_pay', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_fixed_pay', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_variable_pay', models.DecimalField(decimal_places=2, max_digits=10)),
                ('insurance_premiums', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_cost_to_company', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hra', models.DecimalField(decimal_places=2, max_digits=10)),
                ('esic', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('employer_pf_contribution', models.DecimalField(decimal_places=2, max_digits=10)),
                ('flexible_components_tfp', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='WageRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctc', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hra', models.DecimalField(decimal_places=2, max_digits=10)),
                ('esic', models.DecimalField(decimal_places=2, max_digits=10)),
                ('basic_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('conveyance_allowance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('flexible_component', models.DecimalField(decimal_places=2, max_digits=10)),
                ('variable_component', models.DecimalField(decimal_places=2, max_digits=10)),
                ('provident_fund', models.DecimalField(decimal_places=2, max_digits=10)),
                ('professional_tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('income_tax', models.DecimalField(decimal_places=2, default='00', max_digits=10)),
                ('other_deductions', models.DecimalField(decimal_places=2, max_digits=10)),
                ('gross_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_deductions', models.DecimalField(decimal_places=2, max_digits=10)),
                ('net_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('other_allowns', models.DecimalField(decimal_places=2, default='00', max_digits=10)),
                ('lwf', models.DecimalField(decimal_places=2, default='00', max_digits=10)),
                ('ytd_ctc', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_hra', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_esic', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_basic_salary', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_conveyance_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_flexible_component', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_variable_component', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_provident_fund', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_professional_tax', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_income_tax', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_other_deductions', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_gross_salary', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_total_deductions', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_net_salary', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('days_payable', models.IntegerField()),
                ('days_paid', models.IntegerField(null=True)),
                ('address', models.CharField(default='', max_length=500)),
                ('month', models.CharField(default='', max_length=30)),
                ('year', models.CharField(default='', max_length=30)),
                ('age', models.CharField(default='', max_length=20)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wage_registers', to='hr_management_app.employees')),
            ],
        ),
        migrations.CreateModel(
            name='SalarySlip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctc', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hra', models.DecimalField(decimal_places=2, max_digits=10)),
                ('esic', models.DecimalField(decimal_places=2, max_digits=10)),
                ('basic_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('conveyance_allowance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('flexible_component', models.DecimalField(decimal_places=2, max_digits=10)),
                ('variable_component', models.DecimalField(decimal_places=2, max_digits=10)),
                ('provident_fund', models.DecimalField(decimal_places=2, max_digits=10)),
                ('professional_tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('income_tax', models.DecimalField(decimal_places=2, default='00', max_digits=10)),
                ('other_deductions', models.DecimalField(decimal_places=2, max_digits=10)),
                ('gross_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_deductions', models.DecimalField(decimal_places=2, max_digits=10)),
                ('net_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('other_allowns', models.DecimalField(decimal_places=2, default='00', max_digits=10)),
                ('lwf', models.DecimalField(decimal_places=2, default='00', max_digits=10)),
                ('ytd_ctc', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_hra', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_esic', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_basic_salary', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_conveyance_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_flexible_component', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_variable_component', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_provident_fund', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_professional_tax', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_income_tax', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_other_deductions', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_gross_salary', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_total_deductions', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ytd_net_salary', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('days_payable', models.IntegerField()),
                ('days_paid', models.IntegerField(null=True)),
                ('address', models.CharField(default='', max_length=500)),
                ('month', models.CharField(default='', max_length=30)),
                ('year', models.CharField(default='', max_length=30)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salary_slips', to='hr_management_app.employees')),
            ],
        ),
        migrations.CreateModel(
            name='Permanent_Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('per_add_type', models.CharField(choices=[('current', 'Current Address'), ('permanent', 'Permanent Address'), ('other', 'Other Address')], default='perment', max_length=30)),
                ('per_address1', models.CharField(max_length=200)),
                ('per_address2', models.CharField(max_length=200)),
                ('per_zip_code', models.CharField(max_length=6)),
                ('per_city', models.CharField(max_length=100)),
                ('per_dist', models.CharField(max_length=100)),
                ('per_state', models.CharField(default='Maharashtra', max_length=100)),
                ('per_country', models.CharField(max_length=30)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.employees')),
            ],
        ),
        migrations.CreateModel(
            name='OfferLetter_Sended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctc', models.FloatField()),
                ('name', models.CharField(max_length=100)),
                ('offer_release_date', models.DateField()),
                ('joining_date', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=50)),
                ('job_grade', models.IntegerField()),
                ('reporting', models.CharField(max_length=50)),
                ('hr_name', models.CharField(max_length=50)),
                ('offer_accept_date', models.DateField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile_no', models.CharField(max_length=10, unique=True)),
                ('offerletter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.offerletter')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationHRs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('hr_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.hrs')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationEmployee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.employees')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportHR',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_date', models.CharField(max_length=255)),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('hr_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.hrs')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportEmployee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_date', models.DateTimeField(blank=True, max_length=255, null=True)),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('leave_type', models.CharField(max_length=100)),
                ('leave_start_date', models.DateField(max_length=255)),
                ('leave_end_date', models.DateField(max_length=255)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.employees')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBackHRs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField()),
                ('feedback_reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('hr_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.hrs')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBackEmployee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField()),
                ('feedback_reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.employees')),
            ],
        ),
        migrations.CreateModel(
            name='FamilyDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member1_name', models.CharField(max_length=50)),
                ('merber1_dob', models.DateField()),
                ('merber1_aadhar_no', models.CharField(max_length=12)),
                ('relationship1', models.CharField(max_length=50)),
                ('member2_name', models.CharField(max_length=50)),
                ('merber2_dob', models.DateField()),
                ('merber2_aadhar_no', models.CharField(max_length=12)),
                ('relationship2', models.CharField(max_length=50)),
                ('member3_name', models.CharField(max_length=50)),
                ('merber3_dob', models.DateField()),
                ('merber3_aadhar_no', models.CharField(max_length=12)),
                ('relationship3', models.CharField(max_length=50)),
                ('member4_name', models.CharField(blank=True, max_length=50, null=True)),
                ('merber4_dob', models.DateField(blank=True, null=True)),
                ('merber4_aadhar_no', models.CharField(blank=True, max_length=12, null=True)),
                ('relationship4', models.CharField(blank=True, max_length=50, null=True)),
                ('member5_name', models.CharField(blank=True, max_length=50, null=True)),
                ('merber5_dob', models.DateField(blank=True, null=True)),
                ('merber5_aadhar_no', models.CharField(blank=True, max_length=12, null=True)),
                ('relationship5', models.CharField(blank=True, max_length=50, null=True)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.employees')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLeave',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('EarnLeave', models.FloatField(default=0)),
                ('CasualLeave', models.FloatField(default=0)),
                ('TotalLeaves', models.FloatField(default=0)),
                ('EarnLeave_used', models.FloatField(default=0)),
                ('CasualLeave_used', models.FloatField(default=0)),
                ('month_updated', models.IntegerField(default=0)),
                ('year_updated', models.IntegerField(default=0)),
                ('Prev_CFEL', models.FloatField(default=0)),
                ('current_EL', models.FloatField(default=0)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.employees')),
            ],
        ),
        migrations.CreateModel(
            name='Employee_Onboarding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('contact_no', models.CharField(max_length=10)),
                ('emergency_contact_no', models.CharField(max_length=10)),
                ('pancard_no', models.CharField(max_length=10)),
                ('adhaar_no', models.CharField(max_length=12)),
                ('pf_uan_no', models.CharField(max_length=30)),
                ('blood_group', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=20)),
                ('marital_status', models.CharField(choices=[('married', 'Married'), ('unmarried', 'Unmarried')], max_length=30)),
                ('highest_qualification', models.CharField(max_length=50)),
                ('previous_company_name', models.CharField(max_length=30)),
                ('date_of_joining', models.DateField()),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.employees')),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_photo', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('employee_aadhar', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('employee_pan', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('ssc_marksheet', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('hsc_marksheet', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('diploma_marksheet', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('degree_marksheet', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('bank_passbook', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('passport', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('reliving_letter', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('family_member1_aadhar', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('family_member2_aadhar', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('family_member3_aadhar', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('family_member4_aadhar', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('family_member5_aadhar', models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.employees')),
            ],
        ),
        migrations.CreateModel(
            name='BankDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=50)),
                ('branch', models.CharField(max_length=50)),
                ('account_number', models.CharField(max_length=20)),
                ('ifsc_number', models.CharField(max_length=20)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.employees')),
            ],
        ),
        migrations.CreateModel(
            name='AdminHOD',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_type', models.CharField(choices=[('current', 'Current Address'), ('permanent', 'Permanent Address'), ('other', 'Other Address')], default='current', max_length=30)),
                ('address1', models.CharField(max_length=1024)),
                ('address2', models.CharField(max_length=1024)),
                ('zip_code', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=100)),
                ('dist', models.CharField(max_length=100)),
                ('state', models.CharField(default='Maharashtra', max_length=100)),
                ('country', models.CharField(max_length=30)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hr_management_app.employees')),
            ],
        ),
    ]
