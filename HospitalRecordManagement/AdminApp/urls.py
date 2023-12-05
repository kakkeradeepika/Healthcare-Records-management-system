from django.urls import path
from AdminApp import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('AdminAction', views.adminaction),
    path('adminhome', views.adminhome),
    path('AddHsp', views.AddHsp),
    path('AdHSPAction', views.AdHSPAction),
    path('AddDoctor',views.AddDoctor),
    path('AddDoctorAction',views.AddDoctorAction),
    path('BillPatient', views.BillPatient),
    path('ScheduleAppointment', views.ScheduleAppointment),
    path('AddDateTimeAction', views.AddDateTimeAction),
    path('generateBill', views.generateBill),
    path('AddBillAction', views.AddBillAction),
    path('BillPatients', views.BillPatients),
]
