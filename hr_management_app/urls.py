from django.urls import path,re_path
# from .import views
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from hr_management_app import views,EmployeeViews,HRViews,AdminViews,ManagerViews
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView





urlpatterns = [
    path('signup_admin',views.signup_admin,name="signup_admin"),
    path('signup_employee',views.signup_employee,name="signup_employee"),
    path('signup_hr',views.signup_hr,name="signup_hr"),
    path('do_admin_signup',views.do_admin_signup,name="do_admin_signup"),
    path('do_hr_signup',views.do_hr_signup,name="do_hr_signup"),
    path('do_signup_employee',views.do_signup_employee,name="do_signup_employee"),
    path('',views.ShowLoginPage,name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user,name="logout"),
    path('doLogin',views.doLogin,name="do_login"),
    path('admin_home',AdminViews.admin_home,name="admin_home"),
    path('add_hr',AdminViews.add_hr,name="add_hr"),
    path('add_hr_save',AdminViews.add_hr_save,name="add_hr_save"),
    path('add_employee', AdminViews.add_employee,name="add_employee"),
    path('add_employee_save', AdminViews.add_employee_save,name="add_employee_save"),
    path('manage_hr', AdminViews.manage_hr,name="manage_hr"),
    path('manage_employee', AdminViews.manage_employee,name="manage_employee"),
    path('edit_hr/<str:hr_id>', AdminViews.edit_hr,name="edit_hr"),
    path('edit_hr_save', AdminViews.edit_hr_save,name="edit_hr_save"),
    path('edit_employee/<str:employee_id>', AdminViews.edit_employee,name="edit_employee"),
    path('edit_employee_save', AdminViews.edit_employee_save,name="edit_employee_save"),
    path('delete_employee/<str:employee_id>', AdminViews.delete_employee,name='delete_employee'),
    path('employee_details/<int:employee_id>', AdminViews.employee_details,name="employee_details"),
    path('manage_session', AdminViews.manage_session,name="manage_session"),
    path('check_email_exist', AdminViews.check_email_exist,name="check_email_exist"),
    path('check_username_exist', AdminViews.check_username_exist,name="check_username_exist"),
    path('check_mobile_number_exist', AdminViews.check_mobile_number_exist,name="check_mobile_number_exist"),
    path('employee_feedback_message', AdminViews.employee_feedback_message,name="employee_feedback_message"),
    path('employee_feedback_message_replied', AdminViews.employee_feedback_message_replied,name="employee_feedback_message_replied"),
    path('hr_feedback_message', AdminViews.hr_feedback_message,name="hr_feedback_message"),
    path('hr_feedback_message_replied', AdminViews.hr_feedback_message_replied,name="hr_feedback_message_replied"),
    path('employee_leave_view', AdminViews.employee_leave_view,name="employee_leave_view"),
    path('hr_leave_view', AdminViews.hr_leave_view,name="hr_leave_view"),
    path('employee_approve_leave/<str:leave_id>', AdminViews.employee_approve_leave,name="employee_approve_leave"),
    path('employee_disapprove_leave/<str:leave_id>', AdminViews.employee_disapprove_leave,name="employee_disapprove_leave"),
    path('admin_profile', AdminViews.admin_profile,name="admin_profile"),
    path('admin_profile_save', AdminViews.admin_profile_save,name="admin_profile_save"),
    path('admin_send_notification_hr', AdminViews.admin_send_notification_hr,name="admin_send_notification_hr"),
    path('admin_send_notification_employee', AdminViews.admin_send_notification_employee,name="admin_send_notification_employee"),
    path('send_employee_notification', AdminViews.send_employee_notification,name="send_employee_notification"),
    path('send_hr_notification', AdminViews.send_hr_notification,name="send_hr_notification"),
    path('generate_offer_letter', AdminViews.generate_offer_letter, name = 'generate_offer_letter'),





     
                  #     Hr URL Path
    path('hr_home', HRViews.hr_home, name="hr_home"),
    path('delete_hr/<str:hr_id>', AdminViews.delete_hr,name='delete_hr'),
    path('hr_feedback', HRViews.hr_feedback, name="hr_feedback"),
    path('hr_feedback_save', HRViews.hr_feedback_save, name="hr_feedback_save"),
    path('hr_profile', HRViews.hr_profile, name="hr_profile"),
    path('hr_profile_save', HRViews.hr_profile_save, name="hr_profile_save"),
    path('hr_fcmtoken_save', HRViews.hr_fcmtoken_save, name="hr_fcmtoken_save"),
    path('hr_all_notification', HRViews.hr_all_notification, name="hr_all_notification"),

    #    employee 
    path('employee_home', EmployeeViews.employee_home, name="employee_home"),
    path('employee_apply_leave', EmployeeViews.employee_apply_leave, name="employee_apply_leave"),
    path('employee_apply_leave_save', EmployeeViews.employee_apply_leave_save, name="employee_apply_leave_save"),
    path('employee_feedback', EmployeeViews.employee_feedback, name="employee_feedback"),
    path('employee_feedback_save', EmployeeViews.employee_feedback_save, name="employee_feedback_save"),
    path('employee_profile', EmployeeViews.employee_profile, name="employee_profile"),
    path('employee_profile_save', EmployeeViews.employee_profile_save, name="employee_profile_save"),
    path('employee_fcmtoken_save', EmployeeViews.employee_fcmtoken_save, name="employee_fcmtoken_save"),
    # path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
    path('employee_all_notification/',EmployeeViews.employee_all_notification,name="employee_all_notification"),
    path('employee_onboarding',EmployeeViews.EmployeeOnboarding, name='employee_onboarding'),
    path('all_records',EmployeeViews.AllRecords, name='all_records'),
    path('reset_password',views.reset_password, name='reset_password'),
    path('employee_salary_view',EmployeeViews.employee_salary_view, name='employee_salary_view'),
    path('wage_register/',AdminViews.wage_register, name='wage_register'),
    path('wage_register_update/<int:pk>/', AdminViews.edit_wage_register, name='edit_wage_register'),
    path('generate_salary_slips/', AdminViews.generate_salary_slips, name='generate_salary_slips'),
    path('employee_wage_register_details/', AdminViews.employee_wage_register_details, name='employee_wage_register_details'),
    path('offer_letter_sended_history/', AdminViews.offer_letter_sended_history, name='offer_letter_sended_history'),
    path('old_wage_register',AdminViews.old_wage_register, name='old_wage_register'),
    path('payroll', AdminViews.payroll, name='payroll'),
    # re_path(r'^.*/$', RedirectView.as_view(url='/')),


    ###########manager#########
    path('manager_home', ManagerViews.manager_home, name='manager_home'),
    path('do_signup_manager',views.do_signup_manager, name="do_signup_manager"),
    path('signup_manager',views.signup_manager,name="signup_manager"),
    path('manager_profile', ManagerViews.manager_profile, name="manager_profile"),
    path('manager_profile_save', ManagerViews.manager_profile_save, name="manager_profile_save"),
    path('add_manager',AdminViews.add_manager,name="add_manager"),
    path('add_manager_save',AdminViews.add_manager_save,name="add_manager_save"),
    path('manager_leave_view',ManagerViews.manager_leave_view,name="manager_leave_view"),
    path('employee_details_delete/<int:employee_id>', AdminViews.employee_details_delete, name='employee_details_delete'),
    path('password_reset/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('edit_employee_onboarding_record/<int:employee_id>/', AdminViews.edit_employee_onboarding, name='edit_employee_onboarding_record'),

    
]