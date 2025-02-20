from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('profile', views.profile_view, name='profile'),
    path('appointment', views.appointment, name='appointment'),
    path('signup', views.signup, name='signup'),
    path('', views.index, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('contacts/', views.contacts, name='contacts'),
    path('appointment_records/', views.appointment_records, name='appointment_records'),
    path('doctors/', views.doctors, name='doctors'),
    path('about/', views.about_us, name='about_us'),
    path('schedule/', views.schedule_view, name='schedule'),
]

