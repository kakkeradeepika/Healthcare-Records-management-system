from django.urls import path
from Patient import views

urlpatterns = [
    path('login', views.login),
    path('PatientSignup', views.PatientSignup),
    path('PatientRegAction', views.PatientRegAction),
    path('LogAction', views.LogAction),
    path('patienthome', views.patienthome),
    path('viewdoctors', views.viewdoctors),
    path('AppointmentAction', views.AppointmentAction),
    path('BookAppointmentAction', views.BookAppointmentAction),
    path('AppSchedule', views.AppSchedule),
    path('PayBill', views.PayBill),
    path('PBillAction', views.PBillAction),
    path('viewreport', views.viewreport),
    path('helpline', views.helpline),
    path('AddhelpAction', views.AddhelpAction)
]
