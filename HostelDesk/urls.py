from django.contrib import admin
from django.urls import path
from . import views

app_name="HostelDesk"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('change_password/',views.change_password,name="change_password"),
    path('login/',views.login,name="login"),
    path('',views.index,name="index"),
    path('signup/',views.signup,name="signup"),
    path('admin_module/',views.admin_module,name="admin_module"),
    path('ahm/',views.ahm,name="ahm"),
    path('rhm/',views.rhm,name="rhm"),
    path('amm/',views.amm,name="amm"),
    path('rmm/',views.rmm,name="rmm"),
    path('expel_student/',views.expel_student,name="expel_student"),
    path('student_module/',views.student_module,name="student_module"),
    path('application_h/',views.application_h,name="application_h"),
    path('view_enroll_h_rno/',views.view_enroll_h_rno,name="view_enroll_h_rno"),
    path('view_enroll_h_rollno/',views.view_enroll_h_rollno,name="view_enroll_h_rollno"),
    path('application_m/',views.application_m,name="application_m"),
    path('hostel_manager_module/',views.hostel_manager_module,name="hostel_manager_module"),
    path('mess_manager_module/',views.mess_manager_module,name="mess_manager_module"),
    path('view_enroll_m/',views.view_enroll_m,name="view_enroll_m"),
    path('fuc/',views.fuc,name="fuc")
    # path('dash/',views.dash,name="dash"),
]
