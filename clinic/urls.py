from django.urls import path
from . import views

app_name = 'clinic'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clinics/', views.clinic_list, name='clinic_list'),
    path('clinics/<int:pk>/', views.clinic_detail, name='clinic_detail'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('appointment/create/<int:pk>/', views.appointment_create, name='appointment_create'),
    path('doctor/<int:pk>/schedule/create/', views.doctor_schedule_create, name='doctor_schedule_create'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('medical_record/', views.medical_record_list, name='medical_record_list'),
    path('medical_record/<int:pk>/', views.medical_record_detail, name='medical_record_detail'),
]