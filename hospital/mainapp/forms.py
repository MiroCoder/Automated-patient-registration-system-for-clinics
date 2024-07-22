from collections import Counter
from django import forms
from .models import DoctorModel, VisitModel
from .models import AppointmentModel
from django.contrib.auth.forms import UserCreationForm
from .models import ProfileModel
from django.contrib.auth.models import User
from .models import ScheduleModel
from django.db.models import Case, When

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class AppointmentForm(forms.ModelForm):
    date = forms.DateField(label="Дата", widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    doctor = forms.ModelChoiceField(label="Доктор", queryset=DoctorModel.objects.all())

    class Meta:
        model = VisitModel
        fields = ['patient', 'visit_date', 'doctor', 'reason']
        labels = {
            'patient': 'Пациент',
            'date': 'Дата',
            'doctor': 'Доктор',
            'reason': 'Причина'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = DoctorModel.objects.all()
        if user:
            self.fields['patient'].queryset = ProfileModel.objects.filter(user=user)

class PatientForm(forms.ModelForm):
    patient_name = forms.CharField(label="Пациент", max_length=100)
    date = forms.DateField(label="Дата")
    doctor = forms.ModelChoiceField(label="Доктор", queryset=DoctorModel.objects.all())
    class Meta:
        model = AppointmentModel
        fields = ['patient_name', 'date', 'doctor']
        labels = {
            'patient_name': 'Пациент',
            'date': 'Дата',
            'doctor': 'Доктор',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = DoctorModel.objects.all()
        self.fields['patient_name'].queryset = ProfileModel.objects.all()


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)



class ScheduleForm(forms.ModelForm):
    day_of_week = forms.ChoiceField(choices=(
        ('Monday', 'Понедельник'),
        ('Tuesday', 'Вторник'),
        ('Wednesday', 'Среда'),
        ('Thursday', 'Четверг'),
        ('Friday', 'Пятница'),
        ('Saturday', 'Суббота'),
        ('Sunday', 'Воскресенье'),
    ), label='День недели')

    doctors = forms.ModelMultipleChoiceField(queryset=DoctorModel.objects.all(), label='Докторы')

    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Время начала')
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Время конца')

    class Meta:
        model = ScheduleModel
        fields = ['day_of_week', 'doctors', 'start_time', 'end_time']


class VisitForm(forms.ModelForm):
    visit_date = forms.DateField(label="Дата визита", widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    visit_time = forms.TimeField(label="Время визита", widget=forms.widgets.TimeInput(attrs={'type': 'time'}))  # Новое поле

    class Meta:
        model = VisitModel
        fields = ['visit_date', 'visit_time', 'patient', 'doctor', 'reason']
        labels = {
            'visit_date': 'Дата визита',
            'visit_time': 'Время визита',
            'patient': 'Пациент',
            'doctor': 'Доктор',
            'reason': 'Причина',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(VisitForm, self).__init__(*args, **kwargs)


        if user:
            user_profile = user.profilemodel
            visits = VisitModel.objects.filter(patient=user_profile)
            doctor_counts = Counter(visit.doctor for visit in visits)

            sorted_doctors = sorted(doctor_counts.keys(), key=lambda doctor: -doctor_counts[doctor])
            sorted_doctor_ids = [doctor.id for doctor in sorted_doctors]

            remaining_doctors = DoctorModel.objects.exclude(id__in=sorted_doctor_ids)
            preserved_order = Case(*[When(id=doctor_id, then=pos) for pos, doctor_id in enumerate(sorted_doctor_ids)])

            sorted_and_all_doctors = DoctorModel.objects.filter(id__in=sorted_doctor_ids) | remaining_doctors


            self.fields['doctor'].queryset = sorted_and_all_doctors

            self.fields['patient'].initial = user.profilemodel
            self.fields['patient'].queryset = ProfileModel.objects.filter(user=user)
            self.fields['patient'].widget = forms.HiddenInput()
            self.fields['patient'].disabled = True
