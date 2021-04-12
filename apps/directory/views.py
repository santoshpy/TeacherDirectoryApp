import tablib
from django.db.models.functions import Lower, Substr
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, TemplateView

from apps.directory.mixins import LoggedInUserRequired
from apps.directory.models import Subject, Teacher
from apps.directory.resources import TeacherResource
from apps.directory.forms import UserAuthenticationForm


class HomePage(TemplateView):
    template_name = 'home.html'


class UserLoginView(LoginView):
    authentication_form = UserAuthenticationForm
    template_name = "authentication/login.html"
    redirect_authenticated_user = True

class TeacherListView(ListView):
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
        return context

    def get_queryset(self):
        last_name_first_letter = self.request.GET.get("last_name_first_letter")
        subject_name = self.request.GET.get("subject")
        queryset = Teacher.objects.all()
        if last_name_first_letter:
            queryset = queryset.last_name_first_letter(last_name_first_letter)
        if subject_name:
            queryset = queryset.teach(subject_name)
        return queryset


class TeacherDetailView(DetailView):
    model = Teacher
    context_object_name = "teacher"
    template_name = "directory/teacher_detail.html"



class BulkImportView(LoggedInUserRequired, View):
    def get(self, request):
        template_name = "directory/teachers_import.html"
        return render(request, template_name)

    def post(self, request):
        teacher_resource = TeacherResource()
        dataset = tablib.Dataset()
        csv_file = request.FILES["csv_file"]
        upload_images = {fileobj.name: fileobj  for fileobj in request.FILES.getlist('profile_pictures_file')}
        data = dataset.load(csv_file.read().decode(), format="csv")
        result = teacher_resource.import_data(
            data, dry_run=True, raise_errors=True, collect_failed_rows=True,
        )
        if not result.has_errors():
            teacher_resource.import_data(data, dry_run=False, upload_images=upload_images)
            messages.add_message(request, messages.SUCCESS, 'Teacher imported successfully!')

        return redirect('directory:teacher_list')
