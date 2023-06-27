from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.sign_up, name='sign_up'),
    path('sign-in', views.sign_in, name='sign_in'),
    path('logout', views.log_out, name='logout'),
    path('register/teacher', views.register_teacher, name='register_teacher'),
    path('register/student', views.register_student, name='register_student'),
    path('register', views.choose_role, name='choose_role'),
    path('user/teacher/update', views.personal_info, name='personal_teacher_info'),
    # path('user/student/update', views.personal_info_for_student, name='personal_student_info'),
    path('user/student/update', views.personal_info, name='personal_student_info'),
]