import tablib
from django.db.models.functions import Lower, Substr
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from apps.directory.mixins import LoggedInUserRequired
from apps.directory.models import Subject, Teacher
from apps.directory.resources import TeacherResource


class TeacherListView(LoggedInUserRequired, ListView):
    model = Teacher
    context_object_name = "teachers"
    template_name = "directory/teachers_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = (
            Teacher.objects.annotate(last_name_first_char=Lower(Substr("last_name", 1, 1)))
            .values("last_name_first_char")
            .distinct()
            .order_by("last_name_first_char")
        )
        context["last_name_first_letters"] = tuple(
            map(lambda obj: obj.get("last_name_first_char"), qs)
        )
        context["subjects"] = Subject.objects.all()
        print(context)
        return context

    def get_queryset(self):
        last_name_first_letter = self.request.GET.get("last_name_first_char")
        subject_name = self.request.GET.get("subject")
        queryset = Teacher.objects.all()
        if last_name_first_letter:
            queryset = queryset.last_name_first_letter(last_name_first_letter)
        if subject_name:
            queryset = queryset.teach(subject_name)
        return queryset


class TeacherDetailView(LoggedInUserRequired, DetailView):
    model = Teacher
    context_object_name = "teacher"
    template_name = "directory/teacher_detail.html"



class BulkImportView(View):
    def get(self, request):
        template_name = "directory/teachers_import.html"
        return render(request, template_name)

    def post(self, request):
        teacher_resource = TeacherResource()
        dataset = tablib.Dataset()
        csv_file = request.FILES["csv_file"]
        data = dataset.load(csv_file.read().decode(), format="csv")
        result = teacher_resource.import_data(
            data, dry_run=True, raise_errors=True, collect_failed_rows=True
        )
        if not result.has_errors():
            teacher_resource.import_data(data, dry_run=False)
        return render(request, "directory/teachers_import.html")
