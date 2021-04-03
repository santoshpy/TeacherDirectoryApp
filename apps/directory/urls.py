from django.urls import path

from apps.directory.views import BulkImportView

app_name = 'directory'

urlpatterns=[
    path('teacher/bulk_import/', BulkImportView.as_view(), name='bulk-import'),
]