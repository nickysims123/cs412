# File: urls.py
# Name: Nicholas Sima (nicksima@bu.edu)
# Decription: urls file to hold all project urls

from .views import *
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('students/', ShowAllStudentsView.as_view(), name='show_all_students'),
    path('students/add/', CreateStudentView.as_view(), name='create_student'),
    path('students/<int:pk>/edit/', UpdateStudentView.as_view(), name='update_student'),

    path('professors/', ShowAllProfessorsView.as_view(), name='show_all_professors'),
    path('professors/add/', CreateProfessorView.as_view(), name='create_professor'),
    path('professors/<int:pk>/edit/', UpdateProfessorView.as_view(), name='update_professor'),

    path('dorms/', ShowAllDormsView.as_view(), name='show_all_dorms'),
    path('dorms/add/', CreateDormView.as_view(), name='create_dorm'),
    path('dorms/<int:pk>/edit/', UpdateDormView.as_view(), name='update_dorm'),

    path('departments/', ShowAllDepartmentsView.as_view(), name='show_all_departments'),
    path('departments/add/', CreateDepartmentView.as_view(), name='create_department'),
    path('departments/<int:pk>/edit/', UpdateDepartmentView.as_view(), name='update_department'),

    path('hatreds/', ShowAllHatredsView.as_view(), name='show_all_hatreds'),

    path('login/', LoginView.as_view(template_name='project/login.html', next_page='dashboard'), name='login'),
    path('logout/', LogoutView.as_view(next_page='dashboard'), name='logout'),
]
