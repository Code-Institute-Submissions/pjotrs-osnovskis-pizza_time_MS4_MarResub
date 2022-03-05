from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.info, name='info'),
    path('contact/', views.contact_us, name='contact_us'),
]
