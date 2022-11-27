from django.contrib import admin
from django.urls import path
from . import views

app_name="HostelDesk"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name="login"),
    path('',views.index,name="index"),
    path('signup/',views.signup,name="signup"),
    path('admin_module/',views.admin_module,name="admin_module"),
    path('student_module/',views.student_module,name="student_module"),
    path('hostel_manager_module/',views.hostel_manager_module,name="hostel_manager_module"),
    path('mess_manager_module/',views.mess_manager_module,name="mess_manager_module"),
    path('ahm/',views.ahm,name="ahm")
    # path('dash/',views.dash,name="dash"),
]
