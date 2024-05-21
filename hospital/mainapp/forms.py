from django import forms
from .models import DoctorModel
from .models import AppointmentModel
from .models import PatientModel

class AppointmentForm(forms.ModelForm):
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


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)