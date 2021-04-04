from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.directory.models import Subject, Teacher
from apps.directory.resources import TeacherResource


@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    resource_class = TeacherResource


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass
