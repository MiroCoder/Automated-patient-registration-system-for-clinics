from django.contrib import admin
from .models import DoctorModel, ProfileModel,  MedicalRecordModel, ScheduleModel, VisitModel


class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'specialty']
    list_editable = ['name', 'specialty']
    list_filter = ['name', 'specialty']

class VisitAdmin(admin.ModelAdmin):
    list_display = ['id', 'visit_date', 'patient', 'doctor', 'reason']
    list_editable = ['visit_date', 'doctor', 'reason']
    list_filter = ['visit_date', 'patient', 'doctor']

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'creation_date', 'last_update_date', 'diagnosis', 'prescription']
    list_editable = ['patient', 'diagnosis', 'prescription']
    list_filter = ['patient', 'creation_date', 'last_update_date', 'diagnosis', 'prescription']




class ScheduleAdmin(admin.ModelAdmin):
    filter_horizontal = ['doctor']
    list_display = ['day_of_week', 'start_time', 'end_time', 'display_doctors']
    list_filter = ['day_of_week']

    def display_doctors(self, obj):
        return ", ".join([str(doctor) for doctor in obj.doctor.all()])


admin.site.register(ProfileModel)
admin.site.register(DoctorModel, DoctorAdmin)
admin.site.register(VisitModel, VisitAdmin)
admin.site.register(MedicalRecordModel, MedicalRecordAdmin)
admin.site.register(ScheduleModel, ScheduleAdmin)