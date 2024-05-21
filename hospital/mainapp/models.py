import uuid

from django.db import models


class DoctorModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, verbose_name="ФИО")
    specialty = models.CharField(max_length=100, verbose_name="Специальность")

    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'

    def __str__(self):
        return str(self.__dict__)



class PatientModel(models.Model):
    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
    )

    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True,null=True)
    contact_number = models.CharField(max_length=20, verbose_name='Контактный номер', blank=True,null=True)

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'

    def __str__(self):
        return str(self.__dict__)


class AppointmentModel(models.Model):
    patient_name = models.ForeignKey(PatientModel, on_delete=models.SET_NULL, blank=True,null=True)
    date = models.DateField()
    doctor = models.ForeignKey(DoctorModel, on_delete=models.SET_NULL, blank=True,null=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return str(self.__dict__)



class VisitModel(models.Model):
    visit_date = models.DateField()
    patient = models.ForeignKey(PatientModel, on_delete=models.SET_NULL, blank=True,null=True)
    doctor = models.ForeignKey(DoctorModel, on_delete=models.SET_NULL, blank=True,null=True)
    reason = models.TextField()

    def __str__(self):
        return str(self.__dict__)

class ScheduleModel(models.Model):
    doctor = models.ForeignKey(DoctorModel, on_delete=models.SET_NULL, blank=True,null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.__dict__)

class MedicalRecordModel(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.SET_NULL, blank=True,null=True)
    creation_date = models.DateField()
    last_update_date = models.DateField()
    diagnosis = models.TextField()
    prescription = models.TextField()
    visit = models.ForeignKey(VisitModel, on_delete=models.SET_NULL, blank=True,null=True)
    doctor = models.ForeignKey(DoctorModel, on_delete=models.SET_NULL, blank=True,null=True)

    def __str__(self):
        return str(self.__dict__)