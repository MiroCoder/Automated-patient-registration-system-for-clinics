from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('profile', views.profile_view, name='profile'),
    path('appointment', views.appointment, name='appointment')

]