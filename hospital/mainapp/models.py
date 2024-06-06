import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
import datetime
import random

#
# class DoctorModel(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     name = models.CharField(max_length=100, verbose_name="ФИО")
#     specialty = models.CharField(max_length=100, verbose_name="Специальность")
#
#     class Meta:
#         verbose_name = 'Доктор'
#         verbose_name_plural = 'Доктора'
#
#     def __str__(self):
#         return str(self.__dict__)



class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True, verbose_name='Адрес', null=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
    )

    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    contact_number = models.CharField(max_length=20, verbose_name='Контактный номер', blank=True,null=True)


    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'

    def __str__(self):
        return self.full_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        a = ProfileModel.objects.create(user=instance)
        a.save()
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.ProfileModel.save()


class DoctorModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, verbose_name="ФИО")
    specialty = models.CharField(max_length=100, verbose_name="Специальность")
    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'

    def __str__(self):
        return f"{self.name} ({self.specialty})"





class AppointmentModel(models.Model):
    patient_name = models.ForeignKey(ProfileModel, on_delete=models.SET_NULL, blank=True,null=True)
    date = models.DateField()
    doctor = models.ForeignKey(DoctorModel, on_delete=models.SET_NULL, blank=True,null=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return str(self.__dict__)



class VisitModel(models.Model):
    visit_date = models.DateField()
    visit_time = models.TimeField(default=datetime.time(9, 0))
    patient = models.ForeignKey(ProfileModel, on_delete=models.SET_NULL, blank=True,null=True)
    doctor = models.ForeignKey(DoctorModel, on_delete=models.SET_NULL, blank=True,null=True)
    reason = models.TextField()

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return f"{self.visit_date} - {self.patient} - {self.doctor} - {self.reason}"

class ScheduleModel(models.Model):
    doctor = models.ManyToManyField(DoctorModel, blank=True)
    day_of_week = models.CharField(max_length=20, default='Понедельник')
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        return f"{self.doctor} - {self.day_of_week} ({self.start_time} - {self.end_time})"

class MedicalRecordModel(models.Model):
    patient = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, verbose_name='Пациент')
    diagnosis = models.TextField(verbose_name='Диагноз')
    prescription = models.TextField(verbose_name='Рецепт')
    creation_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    last_update_date = models.DateField(auto_now=True, verbose_name='Дата последнего обновления')


    class Meta:
        verbose_name = 'Медицинская карта'
        verbose_name_plural = 'Медицинские карты'
    def __str__(self):
        return str(self.__dict__)