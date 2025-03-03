from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index , name="home"),
    path('process_frame/', views.process_frame, name="process_frame" ),
    path('registration/', views.registration, name="registration"),
    path('person_registration/', views.person_registration, name="person_registration"),
    path('get_detected_person/',views.get_Detected_Person, name="get_Detected_Person")
]
