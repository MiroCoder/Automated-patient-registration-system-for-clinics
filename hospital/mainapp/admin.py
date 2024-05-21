from django.contrib import admin
from .models import DoctorModel

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id','name','specialty']
    list_editable = ['name','specialty']
    list_filter = ['name','specialty']





admin.site.register(DoctorModel,DoctorAdmin)