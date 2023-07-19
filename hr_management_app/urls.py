from django.urls import path,re_path
# from .import views
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from hr_management_app import views,EmployeeViews,HRViews,AdminViews,ManagerViews
from hr_management import settings
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
    # path('add_course/', AdminViews.add_course,name="add_course"),
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
    # path('add_session_save', AdminViews.add_session_save,name="add_session_save"),
    path('check_email_exist', AdminViews.check_email_exist,name="check_email_exist"),
    path('check_username_exist', AdminViews.check_username_exist,name="check_username_exist"),
    path('employee_feedback_message', AdminViews.employee_feedback_message,name="employee_feedback_message"),
    path('employee_feedback_message_replied', AdminViews.employee_feedback_message_replied,name="employee_feedback_message_replied"),
    path('hr_feedback_message', AdminViews.hr_feedback_message,name="hr_feedback_message"),
    path('hr_feedback_message_replied', AdminViews.hr_feedback_message_replied,name="hr_feedback_message_replied"),
    path('employee_leave_view', AdminViews.employee_leave_view,name="employee_leave_view"),
    path('hr_leave_view', AdminViews.hr_leave_view,name="hr_leave_view"),
    path('employee_approve_leave/<str:leave_id>', AdminViews.employee_approve_leave,name="employee_approve_leave"),
    path('employee_disapprove_leave/<str:leave_id>', AdminViews.employee_disapprove_leave,name="employee_disapprove_leave"),
    # path('hr_disapprove_leave/<str:leave_id>', AdminViews.hr_disapprove_leave,name="hr_disapprove_leave"),
    # path('hr_approve_leave/<str:leave_id>', AdminViews.hr_approve_leave,name="hr_approve_leave"),
    # path('admin_view_attendance', AdminViews.admin_view_attendance,name="admin_view_attendance"),
    # path('admin_get_attendance_dates', AdminViews.admin_get_attendance_dates,name="admin_get_attendance_dates"),
    # path('admin_get_attendance_employee', AdminViews.admin_get_attendance_employee,name="admin_get_attendance_employee"),
    path('admin_profile', AdminViews.admin_profile,name="admin_profile"),
    path('admin_profile_save', AdminViews.admin_profile_save,name="admin_profile_save"),
    path('admin_send_notification_hr', AdminViews.admin_send_notification_hr,name="admin_send_notification_hr"),
    path('admin_send_notification_employee', AdminViews.admin_send_notification_employee,name="admin_send_notification_employee"),
    path('send_employee_notification', AdminViews.send_employee_notification,name="send_employee_notification"),
    path('send_hr_notification', AdminViews.send_hr_notification,name="send_hr_notification"),
    # path('all_employee_details',AdminViews.all_employee_details, name='all_employee_details'),
    # path('confirm_delete_employee/<int:employee_id>',AdminViews.confirm_delete_employee, name='confirm_delete_employee'),
    # path('add_employee_payroll/<int:id>', AdminViews.add_employee_payroll, name = 'add_employee_payroll'),
    # path('employee_salary', AdminViews.employee_salary, name = 'employee_salary'),
    path('generate_offer_letter', AdminViews.generate_offer_letter, name = 'generate_offer_letter'),
    # path('enter_ctc', AdminViews.enter_ctc, name = 'enter_ctc'),
    # path('search_wage_register', AdminViews.search_wage_register, name='search_wage_register'),




     
                  #     Hr URL Path
    path('hr_home', HRViews.hr_home, name="hr_home"),
    path('delete_hr/<str:hr_id>', AdminViews.delete_hr,name='delete_hr'),

    # path('hr_take_attendance', HRViews.hr_take_attendance, name="hr_take_attendance"),
    # path('hr_update_attendance', HRViews.hr_update_attendance, name="hr_update_attendance"),
    # path('get_employees', HRViews.get_employees, name="get_employees"),
    # path('get_attendance_dates', HRViews.get_attendance_dates, name="get_attendance_dates"),
    # path('get_attendance_employee', HRViews.get_attendance_employee, name="get_attendance_employee"),
    # path('save_attendance_data', HRViews.save_attendance_data, name="save_attendance_data"),
    # path('save_updateattendance_data', HRViews.save_updateattendance_data, name="save_updateattendance_data"),
    # path('hr_apply_leave', HRViews.hr_apply_leave, name="hr_apply_leave"),
    # path('hr_apply_leave_save', HRViews.hr_apply_leave_save, name="hr_apply_leave_save"),
    path('hr_feedback', HRViews.hr_feedback, name="hr_feedback"),
    path('hr_feedback_save', HRViews.hr_feedback_save, name="hr_feedback_save"),
    path('hr_profile', HRViews.hr_profile, name="hr_profile"),
    path('hr_profile_save', HRViews.hr_profile_save, name="hr_profile_save"),
    path('hr_fcmtoken_save', HRViews.hr_fcmtoken_save, name="hr_fcmtoken_save"),
    path('hr_all_notification', HRViews.hr_all_notification, name="hr_all_notification"),
    # path('hr_add_result', HRViews.hr_add_result, name="hr_add_result"),
    # path('save_employee_result', HRViews.save_employee_result, name="save_employee_result"),
    # path('fetch_result_employee',HRViews.fetch_result_employee, name="fetch_result_employee"),


    #    employee 
    path('employee_home', EmployeeViews.employee_home, name="employee_home"),
    # path('employee_view_attendance', EmployeeViews.employee_view_attendance, name="employee_view_attendance"),
    # path('employee_view_attendance_post', EmployeeViews.employee_view_attendance_post, name="employee_view_attendance_post"),
    path('employee_apply_leave', EmployeeViews.employee_apply_leave, name="employee_apply_leave"),
    path('employee_apply_leave_save', EmployeeViews.employee_apply_leave_save, name="employee_apply_leave_save"),
    path('employee_feedback', EmployeeViews.employee_feedback, name="employee_feedback"),
    path('employee_feedback_save', EmployeeViews.employee_feedback_save, name="employee_feedback_save"),
    path('employee_profile', EmployeeViews.employee_profile, name="employee_profile"),
    path('employee_profile_save', EmployeeViews.employee_profile_save, name="employee_profile_save"),
    path('employee_fcmtoken_save', EmployeeViews.employee_fcmtoken_save, name="employee_fcmtoken_save"),
    path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
    path('employee_all_notification/',EmployeeViews.employee_all_notification,name="employee_all_notification"),
    # path('employee_view_result',EmployeeViews.employee_view_result,name="employee_view_result"),
    path('employee_onboarding',EmployeeViews.EmployeeOnboarding, name='employee_onboarding'),
    path('all_records',EmployeeViews.AllRecords, name='all_records'),


    path('reset_password',views.reset_password, name='reset_password'),
    # path('password_reset_view/', views.CustomPasswordResetView.as_view(), name='password_reset_view'),
    # path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('employee_salary_view',EmployeeViews.employee_salary_view, name='employee_salary_view'),
    # path('employee_salary_all/',AdminViews.employee_salary_all, name='employee_salary_all'),
    path('wage_register/',AdminViews.wage_register, name='wage_register'),
    path('wage_register_update/<int:pk>/', AdminViews.edit_wage_register, name='edit_wage_register'),
    # path('download_excel/', AdminViews.download_excel, name='download_excel'),
    # path('render_wage_register_form/', AdminViews.render_wage_register_form, name='render_wage_register_form'),
    # path('process_wage_register/', AdminViews.process_wage_register, name='process_wage_register'),

    path('generate_salary_slips/', AdminViews.generate_salary_slips, name='generate_salary_slips'),
    path('employee_wage_register_details/', AdminViews.employee_wage_register_details, name='employee_wage_register_details'),
    path('offer_letter_sended_history/', AdminViews.offer_letter_sended_history, name='offer_letter_sended_history'),
    path('old_wage_register',AdminViews.old_wage_register, name='old_wage_register'),
    path('payroll', AdminViews.payroll, name='payroll'),
    re_path(r'^.*/$', RedirectView.as_view(url='/')),





    ###########manager#########
    path('manager_home', ManagerViews.manager_home, name='manager_home'),
    path('do_signup_manager',views.do_signup_manager, name="do_signup_manager"),
    path('signup_manager',views.signup_manager,name="signup_manager"),
    # path('manager_fcmtoken_save', ManagerViews.manager_fcmtoken_save, name="manager_fcmtoken_save"),
    path('manager_profile', ManagerViews.manager_profile, name="manager_profile"),
    path('manager_profile_save', ManagerViews.manager_profile_save, name="manager_profile_save"),
    # path('manager_salary_view', ManagerViews.manager_salary_view, name="manager_salary_view"),
    # path('manager_onboarding', ManagerViews.ManagerOnboarding, name="manager_onboarding"),
    # path('manager_all_records', ManagerViews.ManagerAllRecords, name="manager_all_records"),

    path('add_manager',AdminViews.add_manager,name="add_manager"),
    path('add_manager_save',AdminViews.add_manager_save,name="add_manager_save"),
    # path('manager_approve_leave',ManagerViews.manager_approve_leave,name="manager_approve_leave"),
    path('manager_leave_view',ManagerViews.manager_leave_view,name="manager_leave_view"),
    path('employee_details_delete/<int:employee_id>', AdminViews.employee_details_delete, name='employee_details_delete'),
    path('password_reset/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),
    # path('resend_reset_email', views.resend_reset_email, name='resend_reset_email'),

]