from django.urls import path

from apps.directory.views import BulkImportView

from apps.directory.views import  TeacherListView, TeacherDetailView, HomePage


app_name = "directory"


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path("teacher-list", TeacherListView.as_view(), name="teacher_list"),
    path("teacher-import", BulkImportView.as_view(), name="teacher_import"),
    path("teacher-detail/<slug:slug>", TeacherDetailView.as_view(), name="teacher_detail"),
]
