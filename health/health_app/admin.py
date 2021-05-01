from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from health_app.models import *
# Register your models here.
@admin.register(train,test,disease,symptoms,medicines,doctorlogin,Appoint)
class ViewAdmin(ImportExportModelAdmin):
    pass
# Register your models here.
