from django.urls import path
from Doctors import views

urlpatterns = [
    path('login', views.login),
    path('LogAction', views.LogAction),
    path('home', views.home),
    path('dviewappoint', views.dviewappoint),
    path('GenerateReport', views.GenerateReport),
    path('AddReportAction', views.AddReportAction),
    path('dviewreport', views.dviewreport)
]
