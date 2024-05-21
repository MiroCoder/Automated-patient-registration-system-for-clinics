from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import AppointmentModel, DoctorModel  # Добавлен импорт модели Doctor
from .forms import AppointmentForm, PatientForm
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

@login_required
def profile_view(request):
    print(request.session.__dict__)
    return render(request, 'profile.html', {'user': request.user})

def index(request):
    try:
        session_key = request.session._SessionBase__session_key

        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)

        print(user.__dict__)
    except: pass

    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Аутентификация пользователя
            user = form.get_user()
            login(request, user)
            # Перенаправление пользователя на другую страницу после входа (например, на главную страницу)
            return redirect('index')  # Замените 'home' на имя вашего представления для главной страницы
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(data=request.POST)
        if form.is_valid():
            print(request)
            return redirect('index')
    else:
        form = AppointmentForm()
    return render (request, 'appointment.html', {'form': form})
