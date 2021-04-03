import tablib
from django.shortcuts import render
from django.views import View

from apps.directory.resources import TeacherResource


class BulkImportView(View):
    def get(self, request):
        template_name = "directory/bulk_import.html"
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
        print(result)
        return render(request, "directory/bulk_import.html")
